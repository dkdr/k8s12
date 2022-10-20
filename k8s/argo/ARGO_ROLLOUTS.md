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
curl -LO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64
chmod +x ./kubectl-argo-rollouts-linux-amd64
sudo mv ./kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts
source <(kubectl-argo-rollouts completion bash)
```

Now let's apply initial Rollout and Service (it will automatically scale to 100% since that's an initial install)
```shell
kubectl apply -f rollouts/rollout.yaml
kubectl apply -f rollouts/services.yaml
```
Take a look at [rollout.yaml](rollouts/rollout.yaml) since it describes our rollout startegy. This object is very similar to Deployment and main difference is the `strategy` field. You can even do live migration from Deployment to Rollout without any downtime! To find more follow [this page](https://argoproj.github.io/argo-rollouts/migrating/).

Now we can taka a look at our rollout status:
```shell
kubectl argo rollouts get rollout rollouts-demo
```
You should see 5 running stable pods from one revision. Let's change a little bit :)

It will be nice to take a look at how it looks from user perspective. To do so, we'll need to create an ingress and do one, small trick:
```shell
kubectl apply -f rollouts/ingress.yaml
sudo echo "127.0.0.1 rollouts-demo.local" >> /etc/hosts
```

Now we can take a look at [http://rollours-demo.local](http://rollours-demo.local). You should see some blue squares (each represents one request). Now let's make some mess.

```shell
kubectl argo rollouts set image rollouts-demo rollouts-demo=argoproj/rollouts-demo:yellow
kubectl argo rollouts get rollout rollouts-demo
```

Look once again at [http://rollours-demo.local](http://rollours-demo.local) - there should be exactly 20% of yellow squares. 

But the rollout is not progressing. Why so? Well, there is a pause in our rollout:
```shell
      - setWeight: 20
      - pause: {}
```

Let's get rid of it by promoting our rollout further! (Keep your browser open to see the magic happen)
```shell
kubectl argo rollouts promote rollouts-demo
kubectl argo rollouts get rollout rollouts-demo --watch
```

In your browser you should see, that the rollout is progressing. New version should replace old one in less than minute. This was the simplest example of Canary Deployment. Check this repo later to find Canary Deployment with Prometheus integration :)
