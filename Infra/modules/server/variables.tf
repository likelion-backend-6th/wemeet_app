variable "access_key" {
  type = string
}

variable "secret_key" {
  type = string
}

variable "env" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "name" {
  type = string
}

variable "product_code" {
  type = string
}

variable "init_script_path" {
  type = string
}

variable "init_script_vars" {
  type = map(any)
}

variable "port_range" {
  type = string
}

variable "server_image_code" {
  type = string
}
