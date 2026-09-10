targetScope = 'subscription'

@description('Short environment label used to produce stable, globally unique resource names.')
@minLength(2)
@maxLength(20)
param environmentName string

@description('Azure region for the resource group and application resources.')
param location string

@description('App Service plan SKU. P0v3 is the default production-capable Linux SKU.')
param planSkuName string = 'P0v3'

@description('Origins allowed to make cross-origin browser requests to the API.')
param allowedOrigins array = [
  'http://localhost:3000'
]

var resourceToken = uniqueString(subscription().id, location, environmentName)
var resourceGroupName = 'azrg${resourceToken}'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: resourceGroupName
  location: location
  tags: {
    application: 'task-api'
    environment: environmentName
    managedBy: 'bicep'
  }
}

module application 'app-service.bicep' = {
  scope: resourceGroup
  params: {
    allowedOrigins: allowedOrigins
    environmentName: environmentName
    location: location
    planSkuName: planSkuName
    resourceToken: resourceToken
  }
}

output appName string = application.outputs.appName
output appUrl string = application.outputs.appUrl
output resourceGroupName string = resourceGroup.name
