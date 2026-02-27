group "default" {
  targets = ["helio-core", "web", "telegram-bot", "sfu-rs", "crdt-sync-rs", "reporting-rs", "authz-rs"]
}

target "common" {
  platforms = ["linux/amd64", "linux/arm64"]
}

target "helio-core" {
  inherits = ["common"]
  context = "./core/helio"
}

target "web" {
  inherits = ["common"]
  context = "./apps/web"
}

target "telegram-bot" {
  inherits = ["common"]
  context = "./apps/telegram-bot"
}

target "sfu-rs" {
  inherits = ["common"]
  context = "./microservices/sfu-rs"
}

target "crdt-sync-rs" {
  inherits = ["common"]
  context = "./microservices/crdt-sync-rs"
}

target "reporting-rs" {
  inherits = ["common"]
  context = "./microservices/reporting-rs"
}

target "authz-rs" {
  inherits = ["common"]
  context = "./microservices/authz-rs"
}
