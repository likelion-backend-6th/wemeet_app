output "be_public_ip" {
  value = ncloud_public_ip.be.public_ip
}

output "db_public_ip" {
  value = ncloud_public_ip.db.public_ip
}

# output "be_lb" {
#   value = module.be_lb.dns
# }
