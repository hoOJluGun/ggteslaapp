set shell := ["bash", "-lc"]

build:
	@echo "Building all services"
	docker compose build

dev:
	@echo "Starting dev environment"
	docker compose up -d

prod:
	@echo "Render Helm templates for production"
	helm template ggtesla ./helm/ggtesla

deploy:
	@echo "Apply Argo CD application"
	kubectl apply -f argocd/application.yaml
