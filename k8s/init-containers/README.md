# Init containers

Based on [this](https://github.com/seifrajhi/Kubernetes-practical-exercises-Hands-on/blob/main/init-containers/README.md) exercise.

Here we'll create a pod with init containers, which will try to look for service in our cluster DNS. So they will work after we'll create those services. Useful on daily basis? Not exactly (but in some cases of course, why not?).

```shell
kubectl create namespace initcontainers
kubectl config set-context --current --namespace=initcontainers
kubectl apply -f pod.yaml
sleep 10
kubectl get pods
```

As you can see, the STATUS filed (should be) is a little different than usually. 

```
NAME        READY     STATUS     RESTARTS   AGE
myapp-pod   0/1       Init:0/2   0          6m
```

You can look at `kubectl describe pod myapp-pod`, there you'll see that one (the first one, sequence matters here) init container is Running. And the other one is Waiting.

So let's verify what is happening inside those containers: 

```shell
kubectl logs myapp-pod -c init-myservice # Inspect the first init container
kubectl logs myapp-pod -c init-mydb      # Inspect the second init container
```

As you can see, the logs are available only for the first InitContainer. So now we can create the first service and check what happened.

```shell
kubectl create service clusterip myservice --tcp=80:9376
sleep 5
kubectl get pods
```

As you can see, there is small progress with our deployment, we have `1/2` init containers ready. So now we can create second service.

```shell
kubectl create service clusterip mydb --tcp=80:9377
sleep 5
kubectl get pods
```

## Cleanup

```shell
kubectl delete namespace initcontainers
```