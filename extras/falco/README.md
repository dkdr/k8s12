# Intro

In this example we'll use Falco as a tool to monitor if there is any suspicious** action happening in our cluster.

** - We need to specify rule to catch such event.

# Install and configure Falco

Based on [official example](https://falco.org/docs/getting-started/falco-kubernetes-quickstart/).

```shell
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install --replace falco --namespace falco --create-namespace --set tty=true falcosecurity/falco --wait
```

Falco comes with a [pre-installed](https://falco.org/docs/getting-started/falco-kubernetes-quickstart/) set of rules that alert you upon suspicious behavior.

And now we'll test it:

```shell
kubectl run nginx-falco --image=nginx && sleep 5
kubectl exec -it nginx-falco -- cat /etc/shadow
```

Now we can take a look at Falco logs:
```shell
kubectl logs -l app.kubernetes.io/name=falco -n falco -c falco | grep Warning
```

# Deploy web interface

```shell
helm upgrade --namespace falco falco falcosecurity/falco --set falcosidekick.enabled=true --set falcosidekick.webui.enabled=true --wait
```

And we can access the web interface using credentials `admin`/`admin`:
```shell
kubectl -n falco port-forward svc/falco-falcosidekick-ui 2802
```

http://localhost:2802

After "breaking the law" by running below command, we'll se the evidence in Falcosidekick UI
```shell
kubectl exec -it nginx-falco -- cat /etc/shadow
```

Cleanup
```shell
helm -n falco uninstall falco
```