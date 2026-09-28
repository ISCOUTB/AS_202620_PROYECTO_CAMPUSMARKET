@description('Region permitida por la politica de Azure for Students.')
param location string = 'mexicocentral'

param appServicePlanName string = 'asp-campusmarket-s8'
param webAppName string = 'campusmarket-s8-api-nilver'

param mysqlServerName string = 'campusmarket-s8-mysql-01'
param mysqlDatabaseName string = 'campusmarket'
param mysqlAdministratorLogin string = 'campusmarketadmin'

@secure()
@description('Password del administrador MySQL. Nunca se versiona.')
param mysqlAdministratorPassword string

@description('IPs de salida autorizadas para acceder a MySQL por 3306.')
param allowedDbIps array

resource appServicePlan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: 'F1'
    tier: 'Free'
    capacity: 1
  }
  properties: {
    reserved: true
  }
}

resource mysqlServer 'Microsoft.DBforMySQL/flexibleServers@2025-06-01-preview' = {
  name: mysqlServerName
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: mysqlAdministratorLogin
    administratorLoginPassword: mysqlAdministratorPassword
    createMode: 'Default'
    version: '8.4'
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
    storage: {
      storageSizeGB: 32
      autoGrow: 'Disabled'
      storageRedundancy: 'LocalRedundancy'
    }
  }
}

resource mysqlDatabase 'Microsoft.DBforMySQL/flexibleServers/databases@2023-12-30' = {
  parent: mysqlServer
  name: mysqlDatabaseName
  properties: {
    charset: 'utf8mb4'
    collation: 'utf8mb4_0900_ai_ci'
  }
}

resource webApp 'Microsoft.Web/sites@2024-04-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    publicNetworkAccess: 'Enabled'
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      appCommandLine: 'python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000'
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      scmMinTlsVersion: '1.2'
      httpLoggingEnabled: true
      appSettings: [
        {
          name: 'CAMPUSMARKET_DB_HOST'
          value: '${mysqlServer.name}.mysql.database.azure.com'
        }
        {
          name: 'CAMPUSMARKET_DB_PORT'
          value: '3306'
        }
        {
          name: 'CAMPUSMARKET_DB_USER'
          value: mysqlAdministratorLogin
        }
        {
          name: 'CAMPUSMARKET_DB_PASSWORD'
          value: mysqlAdministratorPassword
        }
        {
          name: 'CAMPUSMARKET_DB_NAME'
          value: mysqlDatabaseName
        }
        {
          name: 'CAMPUSMARKET_DB_SSL'
          value: 'true'
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
      ]
    }
  }
}

resource mysqlFirewallRules 'Microsoft.DBforMySQL/flexibleServers/firewallRules@2023-12-30' = [for (ip, index) in allowedDbIps: {
  parent: mysqlServer
  name: 'AllowAppService${index + 1}'
  properties: {
    startIpAddress: ip
    endIpAddress: ip
  }
}]

output apiUrl string = 'https://${webApp.properties.defaultHostName}'
output healthUrl string = 'https://${webApp.properties.defaultHostName}/health'
output mysqlHost string = '${mysqlServer.name}.mysql.database.azure.com'
