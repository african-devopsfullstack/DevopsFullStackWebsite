resource "kubernetes_service" "this" {
  metadata {
    name      = "${var.container_name}-service"
    namespace = "dev-namespace"
  }
  spec {
    selector = {
      app = kubernetes_deployment.this.metadata.0.labels.app
    }
    session_affinity = "ClientIP"
    port {
      port        = 5000
      target_port = 5000
    }
    type = "NodePort"
  }
}