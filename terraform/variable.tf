variable "image_name" {
  type = string
  description = "Name of the Docker Image"
}

variable "image_tag" {
  type = string
  description = "Tag of Docker Image"
}

variable "container_name" {
  type = string
  description = "Name of the Docker Container"
}

variable "external_port" {
  type = number
  description = "Port to expose the container"
}