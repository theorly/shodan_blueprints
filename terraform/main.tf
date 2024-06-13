terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }
  required_version = ">= 1.1.0"
}
# Providers
provider "azurerm" {
  features {}
  skip_provider_registration = true
}
# RESOURCE-GROUP
resource "azurerm_resource_group" "srs-shodan" {
  name     = "terraform_shodan"
  location = "italynorth"
}
# APP SERVICE PLAN
resource "azurerm_service_plan" "ASP-srs2024stug4-tf" {
  name                = "ASP-srs2024stug4-tf"
  location            = azurerm_resource_group.srs-shodan.location
  resource_group_name = azurerm_resource_group.srs-shodan.name
  os_type             = "Linux"
  sku_name            = "B1"
}
# APP SERVICE PLAN.old
//resource "azurerm_app_service_plan" "ASP-srs2024stug4-tf" {
//  name                = "ASP-srs2024stug4-tf"
//  location            = azurerm_resource_group.srs-shodan.location
//  resource_group_name = azurerm_resource_group.srs-shodan.name
//  kind                = "Linux"
//  reserved            = true
//
//  sku {
//    tier = "Free"
//    size = "F1"
//  }
//}
# USER ASSIGNED IDENTITY
resource "azurerm_user_assigned_identity" "shodan-uai" {
  name                = "shodan-uai"
  resource_group_name = azurerm_resource_group.srs-shodan.name
  location            = azurerm_resource_group.srs-shodan.location
}
# APP #PROVA2
resource "azurerm_app_service" "shodan-webapp" {
  name                = "shodan-webapp"
  resource_group_name = azurerm_resource_group.srs-shodan.name
  location            = azurerm_resource_group.srs-shodan.location
  app_service_plan_id = azurerm_service_plan.ASP-srs2024stug4-tf.id
  depends_on          = [azurerm_application_insights.app_insights_shodan, azurerm_service_plan.ASP-srs2024stug4-tf, azurerm_container_registry.shodan-acr]
  https_only          = true

  site_config {
    app_command_line = ""
    linux_fx_version = "COMPOSE|${filebase64("docker-compose.yml")}"
    http2_enabled    = true
    //health_check_path = "/api/health"
  }

  app_settings = {
    # set application insights
    APPINSIGHTS_INSTRUMENTATIONKEY        = azurerm_application_insights.app_insights_shodan.instrumentation_key
    APPLICATIONINSIGHTS_CONNECTION_STRING = azurerm_application_insights.app_insights_shodan.connection_string
    # add env variables
    DOCKER_REGISTRY_SERVER_PASSWORD     = var.DOCKER_REGISTRY_SERVER_PASSWORD
    DOCKER_REGISTRY_SERVER_URL          = var.DOCKER_REGISTRY_SERVER_URL
    DOCKER_REGISTRY_SERVER_NAME         = var.DOCKER_REGISTRY_SERVER_NAME
    REDIS_HOST                          = var.REDIS_HOST
    REDIS_PORT                          = 6379
    REDIS_PSW                           = var.REDIS_PSW
    SHODAN_API_KEY                      = var.SHODAN_API_KEY
    SQLALCHEMY_DATABASE_URI             = var.SQLALCHEMY_DATABASE_URI
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = var.WEBSITES_ENABLE_APP_SERVICE_STORAGE
    TELEGRAM_BOT_KEY                    = var.TELEGRAM_BOT_KEY
    TELEGRAM_WEBHOOK_URL                = var.TELEGRAM_WEBHOOK_URL
  }

  connection_string {
    name  = "shodanpostgresql"
    type  = "PostgreSQL"
    value = var.connection_string
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.shodan-uai.id]
  }
}

resource "azurerm_monitor_diagnostic_setting" "webapp-diagnostic-tf" {
  name                       = "webapp-diagnostic"
  depends_on                 = [azurerm_app_service.shodan-webapp, azurerm_log_analytics_workspace.log_anayltics_shodan]
  target_resource_id         = azurerm_app_service.shodan-webapp.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_anayltics_shodan.id

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
# REGISTRY UAI
resource "azurerm_user_assigned_identity" "registry" {
  name                = "container-registry"
  resource_group_name = azurerm_resource_group.srs-shodan.name
  location            = azurerm_resource_group.srs-shodan.location
}
# ACR
resource "azurerm_container_registry" "shodan-acr" {
  name                = "shodanTerraformAcr"
  resource_group_name = azurerm_resource_group.srs-shodan.name
  location            = azurerm_resource_group.srs-shodan.location
  depends_on          = []
  sku                 = "Basic"
  #tocheck
  admin_enabled                 = true
  public_network_access_enabled = true
  anonymous_pull_enabled        = false
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.registry.id]
  }
}
# acr permission
resource "azurerm_container_registry_scope_map" "push_pull" {
  name                    = "push-pull"
  description             = "Push and pull permissions for the container registry"
  resource_group_name     = azurerm_resource_group.srs-shodan.name
  depends_on              = [azurerm_container_registry.shodan-acr]
  container_registry_name = azurerm_container_registry.shodan-acr.name
  actions = [
    "repositories/*/content/read",
    "repositories/*/content/write"
  ]
}
# APP.old
//resource "azurerm_webapp" "shodanscanning" {
//  name                = "shodanscanning"
//  resource_group_name = azurerm_resource_group.srs-shodan.name
//  location            = azurerm_resource_group.srs-shodan.location
//  app_service_plan_id = azurerm_app_service_plan.ASP-srs2024stug4-tf.id
//  runtime             = "LINUX"
//  linux_fx_version    = "DOCKER|debian-10"
//  working_dir         = "app"
//  configuration_source = {
//    dockerfile = "Dockerfile"
//    context    = "."
//  }
//  environment {
//    DOCKER_COMPOSE_FILE = "docker-compose.yml"
//    APP_ROOT            = "${azurerm_webapp.shodanscanning.location.name}/${azurerm_webapp.webapp.location.name}"
//  }
//}
# CACHE
resource "azurerm_redis_cache" "shodan-cache-tf" {
  sku_name            = "Basic"
  capacity            = 0
  name                = "shodan-cache-tf"
  location            = azurerm_resource_group.srs-shodan.location
  resource_group_name = azurerm_resource_group.srs-shodan.name
  family              = "C"
  enable_non_ssl_port = false
}
# LOG
resource "azurerm_log_analytics_workspace" "log_anayltics_shodan" {
  name                = "webapp-shodan-logs"
  resource_group_name = azurerm_resource_group.srs-shodan.name
  location            = azurerm_resource_group.srs-shodan.location
  sku                 = "PerGB2018"
  daily_quota_gb      = 1
}
# INSIGHTS
resource "azurerm_application_insights" "app_insights_shodan" {
  name                = "webapp-shodan-insights"
  resource_group_name = azurerm_resource_group.srs-shodan.name
  location            = azurerm_resource_group.srs-shodan.location
  depends_on          = [azurerm_log_analytics_workspace.log_anayltics_shodan]
  workspace_id        = azurerm_log_analytics_workspace.log_anayltics_shodan.id
  application_type    = "other"
}
# POSTGRESQL DB
resource "azurerm_postgresql_flexible_server" "shodanpostgresqlserver" {
  name                = "shodanpostgresqlserver"
  resource_group_name = azurerm_resource_group.srs-shodan.name
  location            = azurerm_resource_group.srs-shodan.location
  version             = "13"
  administrator_login    = var.administrator_login
  administrator_password = var.administrator_password

  zone                  = "1"
  sku_name              = "B_Standard_B1ms"
  storage_mb            = 32768
  backup_retention_days = 7
}

resource "azurerm_postgresql_flexible_server_database" "shodanpostgresqlserver-tf" {
  name      = "shodanpostgresqlserver-tf"
  server_id = azurerm_postgresql_flexible_server.shodanpostgresqlserver.id
  collation = "en_US.utf8"
  charset   = "utf8"

  # prevent destroy
  lifecycle {
    prevent_destroy = true
  }
}

locals {
  postgresql_connection_string = var.connection_string
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "azure" {
  name             = "AllowAzure"
  depends_on       = [azurerm_postgresql_flexible_server.shodanpostgresqlserver]
  server_id        = azurerm_postgresql_flexible_server.shodanpostgresqlserver.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.0"
}
