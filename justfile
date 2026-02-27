set shell := ["bash", "-lc"]

build:
	@echo "Building all services"
	docker compose build

dev:
	@echo "Starting full local environment"
	docker compose up -d

prod:
	@echo "Rendering Helm templates"
	helm template ggtesla ./helm/ggtesla

deploy:
	@echo "Applying Argo CD application"
	kubectl apply -f argocd/application.yaml
