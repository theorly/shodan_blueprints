variable "app_dir" {
  type    = string
  default = "app"
}

variable "repo_name" {
  type        = string
  default     = "theorly/shodan_blueprints"
  description = "The name of the GitHub repository."
}

variable "DOCKER_REGISTRY_SERVER_PASSWORD" {
  type        = string
  description = "Docker registry pw."
  sensitive = true
}

variable "DOCKER_REGISTRY_SERVER_URL" {
  type        = string
  description = "Docker registry connection url."
  sensitive = true
}

variable "DOCKER_REGISTRY_SERVER_NAME" {
  type        = string
  description = "Docker registry server name."
  sensitive = true
}

variable "REDIS_HOST" {
  type        = string
  description = "Redis cache hostname."
  sensitive = true
}

variable "REDIS_PORT" {
  type        = number
  description = "default should be 6379."
  sensitive = true
}

variable "REDIS_PSW" {
  type        = string
  description = "Redis cache password."
  sensitive = true
}

variable "SHODAN_API_KEY" {
  type        = string
  description = "Shodan api key value, keep personal please."
  sensitive = true
}

variable "SQLALCHEMY_DATABASE_URI" {
  type        = string
  description = "Db connection string."
  sensitive = true
}

variable "WEBSITES_ENABLE_APP_SERVICE_STORAGE" {
  type        = string
  description = "Docker registry server name."
  default = "true"
}

variable "TELEGRAM_WEBHOOK_URL" {
  type        = string
  description = "url for webhook."
  sensitive = true
}

variable "TELEGRAM_BOT_KEY" {
  type        = string
  description = "Telegram API key"
  sensitive   = true
}

variable "administrator_login" {
  type        = string
  description = "Admin login for db."
  sensitive = true
}

variable "administrator_password" {
  type        = string
  description = "Pw for db."
  sensitive = true
}

variable "connection_string" {
  type        = string
  description = "string for db connection."
  sensitive = true
}