variable "azurerm_resource_group_name" {
  type        = string
  default     = "srs2024-stu-g4"
  description = "Resource group name."
}

variable "azurerm_storage_name" {
  type        = string
  default     = "shodanpostgresqlserver"
  description = "Name of the db."
}

variable "azurerm_region" {
  type        = string
  default     = "italynorth"
  description = "Azure region to deploy resources."
}

variable "repository" {
  type        = string
  default     = "theorly/shodan_blueprints"
  description = "Name of the GitHub repo."
}

variable "azurerm_webapp_name" {
  type        = string
  default     = "shodanscanning"
  description = "Name of the web app."
}

variable "azurerm_container_name" {
  type        = string
  default     = "shodan"
  description = "Name of the web app."
}

variable "GOOGLE_PROVIDER_AUTHENTICATION_SECRET" {
  type        = string
  description = "GOOGLE_PROVIDER_AUTHENTICATION_SECRET"
  sensitive   = true
}

variable "REDIS_PSW" {
  type        = string
  description = "Redis pw"
  sensitive   = true
}

variable "shodan_api_key" {
  type        = string
  description = "Shodan API key"
  sensitive   = true
}

variable "telegram_api_key" {
  type        = string
  description = "Telegram API key"
  sensitive   = true
}

variable "postgresql_administrator_user" {
  type        = string
  description = "Username for the SQL administrator"
  default     = "psqladmin"
}

variable "postgresql_administrator_password" {
  type        = string
  description = "Password for the SQL administrator"
  sensitive   = true
}