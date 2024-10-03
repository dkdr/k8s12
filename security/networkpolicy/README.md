# NetworkPolicy

In this example we'll deploy and verify some example NetworkPolices based on [this repo](https://github.com/ahmetb/kubernetes-network-policy-recipes).

Of course firstly we need to create a namespace:
```shell
kubectl create namespace netpol
kubectl ns netpol
```

### Limit traffic to application

[Full example](https://github.com/ahmetb/kubernetes-network-policy-recipes/blob/master/02-limit-traffic-to-an-application.md)

Here we'll limit traffic to pod, which will be allowed only from specific pod. Useful if you need to allow traffic to database only from backend pod, or something similar.

Let's start our apiserver, a nginx image which will expose port 80
```shell
kubectl run apiserver --image=nginx --labels="app=bookstore,role=api" --expose --port=80
```

And after a short while we can verify if that's true:
```shell
kubectl run test-123 --rm -it --image=alpine --restart=Never -- wget -qO- --timeout=2 http://apiserver
```

We should get a welcome pagr from nginx, html code of this page to be specific. Now we can try out our networkpolicy, and retry the request.

```shell
kubectl apply -f netpol-01.yaml
kubectl run test-123 --rm -it --image=alpine --restart=Never -- wget -qO- --timeout=2 http://apiserver
```

Now we should see a timeout in request. ([Not working on WSL2](https://github.com/kubernetes-sigs/kind/issues/3705))

```shell
kubectl delete pod apiserver
kubectl delete service apiserver
kubectl delete networkpolicy api-allow
```