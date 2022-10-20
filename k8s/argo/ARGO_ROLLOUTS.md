# Argo Rollouts

Argo Rollouts is a Kubernetes controller and set of CRDs which provide advanced deployment capabilities such as blue-green, canary, canary analysis, experimentation, and progressive delivery features to Kubernetes.

Argo Rollouts (optionally) integrates with ingress controllers and service meshes, leveraging their traffic shaping abilities to gradually shift traffic to the new version during an update. Additionally, Rollouts can query and interpret metrics from various providers to verify key KPIs and drive automated promotion or rollback during an update.

# Install Argo Rollouts

We'll follow [official example](https://argoproj.github.io/argo-rollouts/getting-started/).
As usually, some commands to copy and install needed tools:

```shell
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

We'll also need a kubectl plugin:
```shell
curl -LO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-darwin-amd64
chmod +x ./kubectl-argo-rollouts-darwin-amd64
sudo mv ./kubectl-argo-rollouts-darwin-amd64 /usr/local/bin/kubectl-argo-rollouts
source <(kubectl-argo-rollouts completion bash)
```

Now let's apply initial Rollout and Service (it will automatically scale to 100% since that's an initial install)
```shell
kubectl apply -f rollouts/rollout.yaml
kubectl apply -f rollouts/services.yaml
```
Take a look at [rollout.yaml](https://raw.githubusercontent.com/argoproj/argo-rollouts/master/docs/getting-started/basic/rollout.yaml) since it describes our rollout startegy. This object is very similar to Deployment and main difference is the `strategy` field. You can even do live migration from Deployment to Rollout without any downtime! To find more follow [this page](https://argoproj.github.io/argo-rollouts/migrating/).

