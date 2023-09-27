# ArgoCD

To be able to run this exercise you'll need firstly to install [Helm](_HELM.md)

## Install Argo-CD

Let's start by adding ArgoCD charts repository to our helm instance as described on [ArtifactHub](https://artifacthub.io/packages/helm/argo/argo-cd)

```shell
helm repo add argo https://argoproj.github.io/argo-helm
```

After that we should be able to download our charts:
```shell
helm fetch argo/argo-cd --version 5.46.7
tar xvf argo-cd-5.46.7.tgz
```

By running those commands we'll download our charts and extract them in `argo-cd` directory. You can take a look at `values.yaml` file which should contain whole argocd basic parametrization.

Default values should be fine, so we can just run the installation
```shell
cd argo-cd
kubectl config set-context --current --namespace=default
helm install my-argo-cd . -f values.yaml --atomic
```

## Access the frontend

As described in Argo-CD documentation (and also in `helm install` output) we'll need to get the root password by getting data from k8s Secret object.
```shell
kubectl -n default get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Having this password we should be able to access the frontend. We'll use `kubectl port-forward` to do what it's supposed to do - forward a port to our machine.
```shell
kubectl port-forward service/my-argo-cd-argocd-server -n default 8080:443
```

After that you should be able to acces the Argo-CD frontend by going to [http://localhost:8080/](http://localhost:8080/).

Use username `admin` with password acquired earlier from Secret. Next steps will be described as part of training ;)