resource "docker_container" "this" {
    name = var.container_name
    image = "${var.image_name}:${var.image_tag}"
    ports {
        internal = 5000
        external = var.external_port
    }
}