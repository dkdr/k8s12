# Run your app in your k8s cluster

Let's assume, that you just build app from step described in [docker dir](../docker/simple_app/README.md). If not - well, it will be nice to do so!

First we'll need to load our image to our kind cluster. This step is necessary because of KIND architecture which has no direct access to your local images. If you are a lucky one to have a private repo - then you can push your app image there and work with KIND as you work with your normal k8s cluster. But let's say, that this is not the case here. So lets do the needful
```shell
kind load docker-image app:v1 --name kind
```

By running this command you'll deploy your image to all nodes of KIND cluster. This can take a little longer if you have many workers.

## Run the pod

KIND has access to our docker image, we have the basic kubernetes toolset, so lets try to run our first pod.

To do that you'll need simply to run
```shell
kubectl apply -f pod.yaml
```

You can check if your pod was created by running 
```shell
kubectl get pods
```

You should see, that there are more than 1 pod, but that's fine - they were created by kind and by our ingress controller. You should see, that one of the pods is named `foo-app` and this is the pod we're looking for. 

Let's try to get more info about it! 
```shell
kubectl describe pod foo-app
```

After running this command you should see more information about your pod. You can try to run this command on any other resource on cluster to get more info about it.

## Expose the app

To make the app accessible from outside we'll need to create a Service and an Ingress resource. You can deploy multiple k8s objects from single YAML file with no problem, by running
```shell
kubectl apply -f service-ingress.yaml
```

Same as in previous examples, you can take a closer look at the objects by running some `kubectl describe` commands:
```shell
kubectl get ingress
kubectl describe ingress example-ingress
kubectl get ingress -o wide
kubectl get ingress example-ingress -o yaml 
```

After this, you can verify if tour application is available from outside of cluster by simply running
```shell
curl http://localhost
```

### Do it without YAML files

You can also use kubectl commands to generate YAML files for you, just run
```shell
# Firstly, we'll do some cleanup
kubectl delete pod foo-app
kubectl delete service foo-service
kubectl delete ingress example-ingress

kubectl create deployment test1 --image=app:v2 --replicas 2 
kubectl expose deployment test1 --port 5000 --type ClusterIP
kubectl create ingress app-ingress --rule="/=test1:5000"
```
By that you'll create a deployment instead of single pod deployment. As always, take a look at `kubectl describe` commands.