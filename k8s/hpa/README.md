# Intro

In this example we'll follow [official documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/).

But before proceeding we need to deploy metrics-server which will provide metrics for pods:
```shell
kubectl apply -f metrics-server.yaml
```

Now take a small break for coffee, because metrics-server needs some time for proper startup. 

When you are done taking the break, create a separate namespace and change our context to it:
```shell
kubectl create namespace scaling
kubectl config set-context --current --namespace=scaling
```

# HPA

Next lets create our deployment

```shell
kubectl apply -f php-apache.yaml
```

And crate HPA object:
```shell
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
```

All we need to do is create some load in separate terminal:
```shell
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```

Now lets just watch our pods being scaled up and down (when we stop the `kubectl run` process):
```shell
λ kubectl get hpa php-apache --watch
NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache   55%/50%   1         10        7          10m
```

