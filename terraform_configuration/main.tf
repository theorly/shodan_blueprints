resource "azurerm_resource_group" "shodan_g4" {
  location = var.azurerm_region
  name     = var.azurerm_resource_group_name
}
resource "azurerm_redis_cache" "shodan_cache" {
  capacity            = 0
  enable_non_ssl_port = true
  family              = "C"
  location            = var.azurerm_region
  name                = "shocache"
  resource_group_name = var.azurerm_resource_group_name
  sku_name            = "Basic"
  depends_on = [
    azurerm_resource_group.shodan_g4,
  ]
}
resource "azurerm_container_registry" "shodan_container" {
  admin_enabled       = true
  location            = var.azurerm_region
  name                = var.azurerm_container_name
  resource_group_name = var.azurerm_resource_group_name
  sku                 = "Basic"
  depends_on = [
    azurerm_resource_group.shodan_g4,
  ]
}
resource "azurerm_container_registry_scope_map" "shodan_cont-config1" {
  actions                 = ["repositories/*/metadata/read", "repositories/*/metadata/write", "repositories/*/content/read", "repositories/*/content/write", "repositories/*/content/delete"]
  container_registry_name = var.azurerm_container_name
  description             = "Can perform all read, write and delete operations on the registry"
  name                    = "_repositories_admin"
  resource_group_name     = var.azurerm_resource_group_name
  depends_on = [
    azurerm_container_registry.shodan_container,
  ]
}
resource "azurerm_container_registry_scope_map" "shodan_cont-config2" {
  actions                 = ["repositories/*/content/read"]
  container_registry_name = var.azurerm_container_name
  description             = "Can pull any repository of the registry"
  name                    = "_repositories_pull"
  resource_group_name     = var.azurerm_resource_group_name
  depends_on = [
    azurerm_container_registry.shodan_container,
  ]
}
resource "azurerm_container_registry_scope_map" "shodan_cont-config3" {
  actions                 = ["repositories/*/content/read", "repositories/*/metadata/read"]
  container_registry_name = var.azurerm_container_name
  description             = "Can perform all read operations on the registry"
  name                    = "_repositories_pull_metadata_read"
  resource_group_name     = var.azurerm_resource_group_name
  depends_on = [
    azurerm_container_registry.shodan_container,
  ]
}
resource "azurerm_container_registry_scope_map" "shodan_cont-config4" {
  actions                 = ["repositories/*/content/read", "repositories/*/content/write"]
  container_registry_name = var.azurerm_container_name
  description             = "Can push to any repository of the registry"
  name                    = "_repositories_push"
  resource_group_name     = var.azurerm_resource_group_name
  depends_on = [
    azurerm_container_registry.shodan_container,
  ]
}
resource "azurerm_container_registry_scope_map" "shodan_cont-config5" {
  actions                 = ["repositories/*/metadata/read", "repositories/*/metadata/write", "repositories/*/content/read", "repositories/*/content/write"]
  container_registry_name = var.azurerm_container_name
  description             = "Can perform all read and write operations on the registry"
  name                    = "_repositories_push_metadata_write"
  resource_group_name     = var.azurerm_resource_group_name
  depends_on = [
    azurerm_container_registry.shodan_container,
  ]
}
resource "azurerm_container_registry_webhook" "shodan_webhook" {
  actions             = ["push"]
  location            = var.azurerm_region
  name                = "webappshodanscan"
  registry_name       = var.azurerm_container_name
  resource_group_name = var.azurerm_resource_group_name
  service_uri         = "https://$shodanscan:2Jv9MS3MkE1Aa40jdsq7few0nEs2SWeo8WS4FehY7TxLbN2XmB2wQG8QSmmz@shodanscan.scm.azurewebsites.net/api/registry/webhook"
  depends_on = [
    azurerm_container_registry.shodan_container,
  ]
}
resource "azurerm_postgresql_flexible_server" "shodan_postgresql" {
  location            = var.azurerm_region
  name                = "shodanpostgresqlserver"
  resource_group_name = var.azurerm_resource_group_name
  zone                = "1"
  depends_on = [
    azurerm_resource_group.shodan_g4,
  ]
}
resource "azurerm_postgresql_flexible_server_database" "shodan_db-config1" {
  name      = "azure_maintenance"
  server_id = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.DBforPostgreSQL/flexibleServers/shodanpostgresqlserver"
  depends_on = [
    azurerm_postgresql_flexible_server.shodan_postgresql,
  ]
}
resource "azurerm_postgresql_flexible_server_database" "shodan_db-config2" {
  name      = "azure_sys"
  server_id = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.DBforPostgreSQL/flexibleServers/shodanpostgresqlserver"
  depends_on = [
    azurerm_postgresql_flexible_server.shodan_postgresql,
  ]
}
resource "azurerm_postgresql_flexible_server_database" "shodan_db-config3" {
  name      = "postgres"
  server_id = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.DBforPostgreSQL/flexibleServers/shodanpostgresqlserver"
  depends_on = [
    azurerm_postgresql_flexible_server.shodan_postgresql,
  ]
}
resource "azurerm_postgresql_flexible_server_firewall_rule" "shodan_db-firewall" {
  end_ip_address   = "93.44.203.156"
  name             = "ClientIPAddress_2024-6-2_11-57-3"
  server_id        = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.DBforPostgreSQL/flexibleServers/shodanpostgresqlserver"
  start_ip_address = "93.44.203.156"
  depends_on = [
    azurerm_postgresql_flexible_server.shodan_postgresql,
  ]
}
resource "azurerm_monitor_autoscale_setting" "shodan_autoscale" {
  enabled             = false
  location            = var.azurerm_region
  name                = "app-bqlkmhd6ow4hk-srs2024-stu-g4"
  resource_group_name = var.azurerm_resource_group_name
  target_resource_id  = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.Web/serverfarms/app-bqlkmhd6ow4hk"
  profile {
    name = "Default"
    capacity {
      default = 1
      maximum = 2
      minimum = 1
    }
    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.Web/serverfarms/app-bqlkmhd6ow4hk"
        operator           = "GreaterThan"
        statistic          = "Average"
        threshold          = 80
        time_aggregation   = "Average"
        time_grain         = "PT1M"
        time_window        = "PT10M"
      }
      scale_action {
        cooldown  = "PT10M"
        direction = "Increase"
        type      = "ChangeCount"
        value     = 1
      }
    }
    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.Web/serverfarms/app-bqlkmhd6ow4hk"
        operator           = "LessThan"
        statistic          = "Average"
        threshold          = 60
        time_aggregation   = "Average"
        time_grain         = "PT1M"
        time_window        = "PT1H"
      }
      scale_action {
        cooldown  = "PT1H"
        direction = "Decrease"
        type      = "ChangeCount"
        value     = 1
      }
    }
  }
  depends_on = [
    azurerm_resource_group.shodan_g4,
  ]
}
resource "azurerm_firewall_policy" "shodan_firewall" {
  location            = var.azurerm_region
  name                = "firewall"
  private_ip_ranges   = ["255.255.255.255/32"]
  resource_group_name = var.azurerm_resource_group_name
  threat_intelligence_allowlist {
    fqdns        = ["*"]
    ip_addresses = ["*"]
  }
  depends_on = [
    azurerm_resource_group.shodan_g4,
  ]
}
resource "azurerm_firewall_policy_rule_collection_group" "shodan_firewall-config1" {
  firewall_policy_id = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.Network/firewallPolicies/firewall"
  name               = "DefaultApplicationRuleCollectionGroup"
  priority           = 300
  application_rule_collection {
    action   = "Allow"
    name     = "shodan"
    priority = 1001
    rule {
      destination_fqdns = ["*"]
      name              = "shodan"
      source_addresses  = ["*"]
      protocols {
        port = 3000
        type = "Http"
      }
    }
    rule {
      destination_fqdns = ["shodantry.azurewebsites.net"]
      name              = "promgrafa"
      source_addresses  = ["*"]
      protocols {
        port = 9090
        type = "Http"
      }
    }
  }
  depends_on = [
    azurerm_firewall_policy.shodan_firewall,
  ]
}
resource "azurerm_firewall_policy_rule_collection_group" "shodan_firewall-config2" {
  firewall_policy_id = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.Network/firewallPolicies/firewall"
  name               = "DefaultNetworkRuleCollectionGroup"
  priority           = 200
  depends_on = [
    azurerm_firewall_policy.shodan_firewall,
  ]
}
resource "azurerm_service_plan" "shodan_service-plan" {
  location            = var.azurerm_region
  name                = "ASP-srs2024stug4-b6ef"
  os_type             = "Linux"
  resource_group_name = var.azurerm_resource_group_name
  sku_name            = "B1"
  depends_on = [
    azurerm_resource_group.shodan_g4,
  ]
}
resource "azurerm_linux_web_app" "shodan_webapp" {
  app_settings = {
    DOCKER_ENABLE_CI                      = "true"
    GOOGLE_PROVIDER_AUTHENTICATION_SECRET = var.GOOGLE_PROVIDER_AUTHENTICATION_SECRET
    REDIS_PSW                             = var.REDIS_PSW
    WEBSITES_ENABLE_APP_SERVICE_STORAGE   = "false"
  }
  https_only          = true
  location            = var.azurerm_region
  name                = var.azurerm_webapp_name
  resource_group_name = var.azurerm_resource_group_name
  service_plan_id     = "/subscriptions/fc011c7b-8150-4065-af8b-1a8487bc3f73/resourceGroups/srs2024-stu-g4/providers/Microsoft.Web/serverFarms/ASP-srs2024stug4-b6ef"
  auth_settings_v2 {
    require_authentication = true
    unauthenticated_action = "AllowAnonymous"
    active_directory_v2 {
      client_id            = ""
      tenant_auth_endpoint = ""
    }
    apple_v2 {
      client_id                  = ""
      client_secret_setting_name = ""
    }
    facebook_v2 {
      app_id                  = ""
      app_secret_setting_name = ""
    }
    github_v2 {
      client_id                  = ""
      client_secret_setting_name = ""
    }
    google_v2 {
      client_id                  = ""
      client_secret_setting_name = ""
    }
    login {
      logout_endpoint     = "/.auth/logout"
      token_store_enabled = true
    }
    microsoft_v2 {
      client_id                  = ""
      client_secret_setting_name = ""
    }
    twitter_v2 {
      consumer_key                 = ""
      consumer_secret_setting_name = ""
    }
  }
  site_config {
    always_on                         = false
    ftps_state                        = "FtpsOnly"
  }
  sticky_settings {
    app_setting_names = ["GOOGLE_PROVIDER_AUTHENTICATION_SECRET"]
  }
  depends_on = [
    azurerm_service_plan.shodan_service-plan,
  ]
}
resource "azurerm_app_service_custom_hostname_binding" "shodan_webapp-custom-hostname" {
  app_service_name    = var.azurerm_webapp_name
  hostname            = "shodanscanning.azurewebsites.net"
  resource_group_name = var.azurerm_resource_group_name
  depends_on = [
    azurerm_linux_web_app.shodan_webapp,
  ]
}
