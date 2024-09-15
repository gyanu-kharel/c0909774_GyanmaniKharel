provider "azurerm" {
  features {}

  client_id       = var.AZURE_CLIENT_ID
  client_secret   = var.AZURE_CLIENT_SECRET
  tenant_id       = var.AZURE_TENANT_ID
  subscription_id = var.AZURE_SUBSCRIPTION_ID
}

resource "azurerm_resource_group" "aks_rg" {
  name     = "todoapprg"
  location = "East US"
}

resource "azurerm_kubernetes_cluster" "aks_cluster" {
  name                = "todoappcluster"
  location            = azurerm_resource_group.aks_rg.location
  resource_group_name = azurerm_resource_group.aks_rg.name
  dns_prefix          = "todo"

  default_node_pool {
    name       = "default"
    node_count = 1  
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "development"
  }
}

terraform {
  backend "azurerm" {
    resource_group_name  = "todoapp"
    storage_account_name = "todostoragegyan" 
    container_name       = "tfstates"
    key                  = "terraform.tfstate"
  }
}
