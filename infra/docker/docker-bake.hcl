group "default" {
  targets = ["helio-core", "telegram-bot", "web"]
}

target "helio-core" {
  context = "./core/helio"
  dockerfile = "Dockerfile"
  platforms = ["linux/amd64", "linux/arm64"]
  tags = ["ggtesla/helio-core:latest"]
}

target "telegram-bot" {
  context = "./apps/telegram-bot"
  dockerfile = "Dockerfile"
  platforms = ["linux/amd64", "linux/arm64"]
  tags = ["ggtesla/telegram-bot:latest"]
}

target "web" {
  context = "./apps/web"
  dockerfile = "Dockerfile"
  platforms = ["linux/amd64", "linux/arm64"]
  tags = ["ggtesla/web:latest"]
}
