

create-cluster:
	kind create cluster --config=kind.yaml

deploy-ambassador:
	kubectl apply -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-crds.yaml
	kubectl apply -n ambassador -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-kind.yaml
	kubectl wait --timeout=180s -n ambassador --for=condition=deployed ambassadorinstallations/ambassador

deploy-prometheus:
	kubectl create ns prometheus
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo update
	helm install prometheus prometheus-community/prometheus-operator -n prometheus
	kubectl apply -n prometheus -f .\.k8s\prometheus-ingress.yaml
	kubectl annotate -n prometheus ingress prometheus-operated kubernetes.io/ingress.class=ambassador

deploy-php-apache:
	kubectl create ns guestbook
	kubectl apply -n guestbook -f .\.k8s\php-apache.yaml
	# kubectl wait -n guestbook  --timeout=180s --for=condition=deployed php-apache/php-apache
	kubectl apply -n guestbook -f .\.k8s\php-apache-load.yaml