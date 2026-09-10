[CmdletBinding()]
param(
    [Parameter()]
    [ValidatePattern('^[a-z]{1,5}$')]
    [string]$ResourceToken,

    [Parameter()]
    [ValidatePattern('^[a-z][a-z0-9]{1,14}$')]
    [string]$EnvironmentName = 'workshop',

    [Parameter()]
    [string]$Location = 'eastus2',

    [Parameter()]
    [string]$PlanSkuName = 'P0v3',

    [Parameter()]
    [string]$SubscriptionId,

    [Parameter()]
    [switch]$Preview
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version Latest

function Assert-LastCommandSucceeded {
    param([Parameter(Mandatory)][string]$Action)

    if ($LASTEXITCODE -ne 0) {
        throw "$Action failed with exit code $LASTEXITCODE."
    }
}

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    throw 'Azure CLI (az) is required. Install it and run az login before using this script.'
}

$projectRoot = Split-Path -Parent $PSScriptRoot
$stateDirectory = Join-Path $projectRoot '.azure'
$tokenFile = Join-Path $stateDirectory 'resource-token.txt'

if ([string]::IsNullOrWhiteSpace($ResourceToken)) {
    if (Test-Path $tokenFile) {
        $ResourceToken = (Get-Content $tokenFile -Raw).Trim()
    }
    else {
        $ResourceToken = -join (1..5 | ForEach-Object { [char](Get-Random -Minimum 97 -Maximum 123) })
        New-Item -ItemType Directory -Path $stateDirectory -Force | Out-Null
        Set-Content -Path $tokenFile -Value $ResourceToken -NoNewline
    }
}

if ($ResourceToken -notmatch '^[a-z]{1,5}$') {
    throw 'ResourceToken must contain one to five lowercase letters.'
}

$deploymentEnvironment = "$EnvironmentName$ResourceToken"
if ($deploymentEnvironment.Length -gt 20) {
    throw 'EnvironmentName plus ResourceToken must not exceed 20 characters.'
}

if ([string]::IsNullOrWhiteSpace($SubscriptionId)) {
    $SubscriptionId = az account show --query id --output tsv
    Assert-LastCommandSucceeded 'Reading the active Azure subscription'
}

az account set --subscription $SubscriptionId
Assert-LastCommandSucceeded 'Selecting the Azure subscription'

$availableLocations = az appservice list-locations --sku $PlanSkuName --query '[].name' --output tsv
Assert-LastCommandSucceeded "Checking $PlanSkuName availability"
$normalizedLocation = $Location.Replace(' ', '').ToLowerInvariant()
$locationAvailable = $availableLocations | Where-Object {
    $_.Replace(' ', '').ToLowerInvariant() -eq $normalizedLocation
}
if (-not $locationAvailable) {
    throw "App Service SKU $PlanSkuName is not available in $Location for this subscription."
}

$pythonRuntimes = az webapp list-runtimes --os linux --output tsv
Assert-LastCommandSucceeded 'Checking Linux Python runtime availability'
if ($pythonRuntimes -notcontains 'PYTHON|3.14') {
    throw 'The PYTHON:3.14 App Service runtime is not currently available.'
}

$deploymentName = "azdep$ResourceToken"
$parametersFile = Join-Path $PSScriptRoot 'main.parameters.json'
$templateFile = Join-Path $PSScriptRoot 'main.bicep'
$parameterFileArgument = "@$parametersFile"

$deploymentExist = az deployment sub show --name $deploymentName --query name --output tsv 2>$null
Write-Verbose "Existing deployment lookup result: $deploymentExist"
if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($deploymentExist)) {
    Write-Host "Updating existing deployment $deploymentName."
}
else {
    Write-Host "Creating deployment $deploymentName."
}

$deploymentArguments = @(
    '--name', $deploymentName,
    '--location', $Location,
    '--template-file', $templateFile,
    '--parameters', $parameterFileArgument,
    "environmentName=$deploymentEnvironment",
    "location=$Location",
    "planSkuName=$PlanSkuName"
)

if ($Preview) {
    az deployment sub what-if @deploymentArguments
    Assert-LastCommandSucceeded 'Previewing the subscription deployment'
    return
}

az deployment sub create @deploymentArguments --output table
Assert-LastCommandSucceeded 'Deploying the Azure infrastructure'

$outputsJson = az deployment sub show --name $deploymentName --query properties.outputs --output json
Assert-LastCommandSucceeded 'Reading deployment outputs'
$outputs = $outputsJson | ConvertFrom-Json
$appName = $outputs.appName.value
$appUrl = $outputs.appUrl.value
$resourceGroupName = $outputs.resourceGroupName.value

$webAppExist = az webapp show --name $appName --resource-group $resourceGroupName --query name --output tsv 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($webAppExist)) {
    throw "The expected App Service $appName was not found after deployment."
}

$packageRoot = Join-Path ([System.IO.Path]::GetTempPath()) "task-api-$ResourceToken"
$zipPath = Join-Path ([System.IO.Path]::GetTempPath()) "task-api-$ResourceToken.zip"

try {
    Remove-Item $packageRoot -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path $packageRoot -Force | Out-Null

    Copy-Item (Join-Path $projectRoot 'app') -Destination $packageRoot -Recurse
    Copy-Item (Join-Path $projectRoot 'requirements.txt') -Destination $packageRoot
    Compress-Archive -Path (Join-Path $packageRoot '*') -DestinationPath $zipPath -Force

    az webapp deploy `
        --name $appName `
        --resource-group $resourceGroupName `
        --src-path $zipPath `
        --type zip `
        --track-status false `
        --output table
    Assert-LastCommandSucceeded 'Deploying the FastAPI application'
}
finally {
    Remove-Item $packageRoot -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
}

Write-Host ''
Write-Host 'Deployment submitted successfully.'
Write-Host "Application: $appUrl"
Write-Host "Health:      $appUrl/health"
Write-Host "API docs:    $appUrl/docs"
Write-Host 'Allow two to three minutes for the first build and startup.'
