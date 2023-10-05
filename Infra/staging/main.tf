terraform {
  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
    }
    ssh = {
      source  = "loafoe/ssh"
      version = "2.6.0"
    }
  }
  required_version = ">= 0.13"
}

provider "ncloud" {
  access_key  = var.access_key
  secret_key  = var.secret_key
  region      = "KR"
  site        = "PUBLIC"
  support_vpc = true
}

locals {
  env               = "staging"
  server_image_code = "SW.VSVR.OS.LNX64.UBNTU.SVR2004.B050"
  db_port           = "5432"
  be_port           = "8000"
}

module "network" {
  source = "../modules/network"

  secret_key = var.secret_key
  access_key = var.access_key
  env        = local.env
}

module "db_server" {
  source = "../modules/server"

  secret_key        = var.secret_key
  access_key        = var.access_key
  env               = local.env
  vpc_id            = module.network.vpc_id
  subnet_id         = module.network.subnet_id
  name              = "db"
  server_image_code = local.server_image_code
  product_code      = data.ncloud_server_products.products.server_products[0].product_code
  init_script_path  = "db_init_script.tftpl"
  init_script_vars = {
    password    = var.password
    db          = var.db
    db_user     = "postgres"
    db_password = var.db_password
    db_port     = local.db_port
  }
  port_range = local.db_port
}

module "be_server" {
  source = "../modules/server"

  secret_key        = var.secret_key
  access_key        = var.access_key
  env               = local.env
  vpc_id            = module.network.vpc_id
  subnet_id         = module.network.subnet_id
  name              = "be"
  server_image_code = local.server_image_code
  product_code      = data.ncloud_server_products.products.server_products[0].product_code
  init_script_path  = "be_init_script.tftpl"
  init_script_vars = {
    password               = var.password
    db                     = var.db
    db_user                = "postgres"
    db_password            = var.db_password
    db_port                = local.db_port
    db_host                = ncloud_public_ip.db.public_ip
    django_settings_module = "meet.config.staging"
    django_secret_key      = var.django_secret_key
  }
  port_range = local.be_port
}

resource "ncloud_public_ip" "be" {
  server_instance_no = module.be_server.instance_no
}

resource "ncloud_public_ip" "db" {
  server_instance_no = module.db_server.instance_no
}

resource "ssh_resource" "init_db" {
  depends_on = [module.db_server]
  when       = "create"

  host     = ncloud_public_ip.db.public_ip
  user     = "lion"
  password = var.password

  timeout     = "1m"
  retry_delay = "5s"

  file {
    content     = "${path.module}/set_db_server.sh"
    destination = "/home/lion/init.sh"
    permissions = "0700"
  }

  commands = [
    "echo 'SSH conncetion successful'",
    "/home/lion/init.sh"
  ]
}

resource "ssh_resource" "init_be" {
  depends_on = [module.be_server]
  when       = "create"

  host     = ncloud_public_ip.be.public_ip
  user     = "lion"
  password = var.password

  timeout     = "1m"
  retry_delay = "5s"

  file {
    content     = "${path.module}/set_be_server.sh"
    destination = "/home/lion/init.sh"
    permissions = "0700"
  }

  commands = [
    "echo 'SSH conncetion successful'",
    "/home/lion/init.sh"
  ]
}

data "ncloud_server_products" "products" {
  server_image_product_code = local.server_image_code

  filter {
    name   = "product_code"
    values = ["SSD"]
    regex  = true
  }

  filter {
    name   = "cpu_count"
    values = ["2"]
  }

  filter {
    name   = "memory_size"
    values = ["4GB"]
  }

  filter {
    name   = "base_block_storage_size"
    values = ["50GB"]
  }

  filter {
    name   = "product_type"
    values = ["HICPU"]
  }
}
