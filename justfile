default:
    @just --list

build:
    docker compose build

dev:
    docker compose up -d

prod:
    helm template ggtesla ./helm/ggtesla

deploy:
    kubectl apply -f argocd/application.yaml

test:
    bash tests/smoke.sh

clean:
    docker compose down -v
