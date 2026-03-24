provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "my-rag-resources"
  location = "East US"
}

resource "azurerm_storage_account" "storage" {
  name                     = "ragstorage${random_id.suffix.hex}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "container" {
  name                  = "my-container"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "random_id" "suffix" {
  byte_length = 4
}

output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "container_name" {
  value = azurerm_storage_container.container.name
}