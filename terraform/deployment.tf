resource "kubernetes_deployment" "this" {
  metadata {
    name      = "${var.container_name}-deployment"
    namespace = "dev-namespace"
    labels = {
      app = "${var.container_name}-deployment"
    }
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "${var.container_name}-deployment"
      }
    }
    template {
      metadata {
        labels = {
          app = "${var.container_name}-deployment"
        }
      }
      spec {
        container {
          image = "${var.image_name}:${var.image_tag}"
          name  = "${var.container_name}-container"

          resources {
            limits = {
              cpu    = "0.5"
              memory = "50Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
          port {
            container_port = 5000
          }
        }
        restart_policy = "Always"
      }

    }
  }
}