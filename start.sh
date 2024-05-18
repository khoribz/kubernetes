minikube start

chmod +x istio/start_istio.sh
./istio/start_istio.sh

kubectl apply -f postgres/manifests/config.yml
kubectl apply -f postgres/manifests/deployment.yml
kubectl apply -f postgres/manifests/service.yml

kubectl rollout status deployment/postgres-deployment --timeout=300s

kubectl apply -f statistic_app/manifests/deployment.yml
kubectl apply -f statistic_app/manifests/service.yml

kubectl apply -f statistics_collector/manifests/deployment.yml
kubectl apply -f statistics_collector/manifests/service.yml

kubectl rollout status deployment/app-deployment --timeout=300s

kubectl apply -f istio/manifests/virtual_service.yml
kubectl apply -f istio/manifests/gateway.yml
kubectl apply -f istio/manifests/service_entry.yml

minikube service app-service --url