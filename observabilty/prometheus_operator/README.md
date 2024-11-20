# Prometheus

Prometheus is a monitoring system which consist of several components. The main one is a prometheus server which is responsible for data retrieval, data storing, querying and alerting. However, alert routing is usually done by Alertmanager. Prometheus server also ships with a simple Web UI. 

# Prometheus operator

To make the deployment of prometheus easy we'll use prometheus operator, which is a tool to simplify deployment of prometheus. It allows us not only to deploy prometheus instance, but it will also help us to manage it.

# Kube-prometheus-stack

We're talking about prometheus, prometheus-operator, and now we're at kube-prometheus-stack. This is a collection of tools which is suitable to deploying full stack kubernetes cluster monitoring. It implements simple way to deploy prometheus-operator, which deploys prometheus itself, but also has built-in grafana and some nice grafana dashboards.

Enough theory, lets deploy it!

# Deployment

As in most cases, we'll use Artifacthub to get our charts. You can find more info [here](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack).

Let's add the repo, and fetch the charts:

```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm fetch prometheus-community/kube-prometheus-stack --version 66.2.1
tar xvf kube-prometheus-stack-66.2.1.tgz
cd kube-prometheus-stack/
```

We don't need to change any default values to make it work, however it is a good idea to take a closer look at `values.yaml` file. It is nicely documented. Basic config will allow us to deploy grafana with dashboards, and prometheus with some alerts, so let's proceed:

```shell
kubectl create namespace monitoring
kubectl config set-context --current --namespace=monitoring
helm install kube-monitoring -f values.yaml . --wait --atomic
```

Now we only need to access the UIs.

## Access frontend

To access grafana ui:
```shell
kubectl port-forward service/kube-monitoring-grafana 9080:80
```

You'll find grafana under [http://localhost:9080/](http://localhost:9080/). 

Default login/password for grafana: `admin:prom-operator`.

You can take a look at example dashboards. Note that some dashboards might not work out of the box (for example: etcd dashboard). This is fine.

And you can do the same for prometheus ui:
```shell
kubectl port-forward service/kube-monitoring-kube-prome-prometheus 9090:9090
```
You'll find default alerts under [http://localhost:9090/alerts](http://localhost:9090/alerts). Some alerts can be already Firing, but there is nothing to worry about - this is a default deployment which might not be exact fit for your cluster.

Take a look also at target section: [http://localhost:9090/targets](http://localhost:9090/targets). 

# What's next?

So you just deployed full-stack monitoring for your cluster. There are some small fixes depending on your cluster configuration, but this should be a good start. Let's go one step further - let's deploy custom app with it's own metrics, make it discoverable by prometheus and let's create an alert for this. [Follow me](./ALERT.md).