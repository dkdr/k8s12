# Intro

To create some custom alert we'll need to deploy an application with custom metrics. We'll follow example described in [Tanzu dev guide](https://tanzu.vmware.com/developer/guides/spring-prometheus/) which deploys simple springboot app with visitor count metric. It'll allow us to trigger the alarm by simply visiting the site.

# Deploy

This example is a set of simple YAML files, so nothing fancy here.

```shell
curl -o springboot.yaml https://raw.githubusercontent.com/BrianMMcClain/spring-prometheus-demo/main/deploy.yaml
kubectl apply -f springboot.yaml
```

Take a look what you jus deployed (usually you should do this before deployment, but here we are). You can find Deployment object, Service object and ServiceMonitor object. Latest one is something new - this object is automagically scraped by prometheus-operator and it should be injected into prometheus configuration. Should be...

```shell
kubectl label servicemonitor spring-prometheus-demo-service-monitor "release=kube-monitoring"
```

Once again, we ran some code and get explanation later - above command adds label to our ServiceMonitor object which will allow our default prometheus-operator deployment to find it and add it to prometheus configuration. This is done because of default prometheus-operator configuration. You can change the selector in kube-prometheus-stack `values.yaml` file, but if you do so, don't forget about default ServiceMonitors!

## Other namespaces

Ok, this works fine, because we're in the same namespace. But what if we're not? Well in this case we need to take a look into `values.yaml` file from `kube-prometheus-stack`. We need to look at `serviceMonitorNamespaceSelector` section and make some changes. This parameter is responsible for telling prometheus operator about which namespaces it should watch for new `ServiceMonitor` objects. So lets set it to some label:
```shell
helm upgrade kube-monitoring -f values.yaml . --wait --set prometheus.prometheusSpec.serviceMonitorNamespaceSelector.matchLabels.prometheus=enabled
```

Take a sip of coffee, think about your holidays plans, and after 30-60 seconds you should see a difference in prometheus target section - it will be empty! We need to do something with it (or we can leave it as it is, go to sleep, and leave it to someone else...). If we set a `NamespaceSelector` we need also to set a label to our `monitoring` namespace:
```shell
kubectl label namespace monitoring prometheus=enabled
```

And now everything should be back to normal. Note that this configuration applies to "default" prometheus instance deployed by this chart. You can deploy multiple instances with its own selectors.

## Grafana Dashboard

If you deployed the ServiceMonitor you should be able to find new target in prometheus configuration. Now we need to import [this dashboard](https://grafana.com/grafana/dashboards/4701) 

# Alert

To deploy the alert you simply need to, as usually, deploy a YAML file:

```shell
kubectl apply -f alert.yaml
```