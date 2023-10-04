terraform {
  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
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

resource "ncloud_lb" "main" {
  name         = "${var.name}-lb-${var.env}"
  network_type = "PUBLIC"
  type         = "NETWORK_PROXY"
  subnet_no_list = [
    ncloud_subnet.main.id,
  ]
}

data "ncloud_vpc" "main" {
  id = var.vpc_id
}

resource "ncloud_subnet" "main" {
  vpc_no         = var.vpc_id
  subnet         = cidrsubnet(data.ncloud_vpc.main.ipv4_cidr_block, 10, 3)
  zone           = "KR-2"
  network_acl_no = data.ncloud_vpc.main.default_network_acl_no
  subnet_type    = "PRIVATE"
  name           = "lion-sbn-lb-${var.env}"
  usage_type     = "LOADB"
}

resource "ncloud_lb_listener" "main" {
  load_balancer_no = ncloud_lb.main.load_balancer_no
  protocol         = "TCP"
  port             = 80
  target_group_no  = ncloud_lb_target_group.main.target_group_no
}

resource "ncloud_lb_target_group" "main" {
  vpc_no      = var.vpc_id
  protocol    = "PROXY_TCP"
  target_type = "VSVR"
  port        = 8000
  health_check {
    protocol       = "TCP"
    http_method    = "GET"
    port           = 8000
    url_path       = "/admin"
    cycle          = 30
    up_threshold   = 2
    down_threshold = 2
  }
  algorithm_type = "RR"
}

resource "ncloud_lb_target_group_attachment" "main" {
  target_group_no = ncloud_lb_target_group.main.id
  target_no_list = [
    var.instance_no
  ]
}
