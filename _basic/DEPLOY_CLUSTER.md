# Deploying k8s cluster

In our scenario we'll deploy cluster which consist of 3 masters, and 3 workers. You can change amount of masters/workers by editing [cluster.yaml](cluster.yaml) file.

To deploy our cluster we'll simply need the [cluster.yaml](cluster.yaml) file, and of course all those previous tools and commands.

To deploy our cluster we just need to run:

```shell
kind create cluster --config cluster.yaml
```

Kind will need some time to download the images and start the workers, it usually takes up tu 3 minutes.

After that we can check if our cluster is avaliable:
```shell
kubectl version
```

After running above command we should get response which consist of our local kubectl version and cluster version.

If everything works fine we'll proceed to deploy ingress-controller on our cluster. Lets run:

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
```

And then, we'll need to wait some time for it to be ready. We can check if our ingress controller is ready by running:

```shell
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

# Reacreating cluster

If you had any problems with your cluster you can simply delete it by running
```shell
kind delete cluster
```

Kind will then delete you cluster and you can run all commands above once again to create a new, fresh cluster (ok, you can skip tke `kubectl version` command).