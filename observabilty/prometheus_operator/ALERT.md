# Intro

To create some custom alert we'll need to deploy an application with custom metrics. We'll follow example described in [Tanzu dev guide](https://tanzu.vmware.com/developer/guides/spring-prometheus/) which deploys simple springboot app with visitor count metric. It'll allow us to trigger the alarm by simply visiting the site.

# Deploy

This example is a set of simple YAML files, so nothing fancy here.

```shell
curl -o springboot.yaml https://raw.githubusercontent.com/BrianMMcClain/spring-prometheus-demo/main/deploy.yaml
oc apply -f springboot.yaml
```

Here you'll experience a permission error if you're using normal user. But worry not! There is a simple way to fix the issue, all you need to do is... grant those permissions!

```shell
oc policy add-role-to-user monitoring-edit <user namespace>> -n <user name>
```

After re-running previous command, you can visit `Observe -> Metrics` section and in query select `Custom Query` then type `visit_counter_total`

# Alert

To deploy the alert you simply need to, as usually, deploy a YAML file:

```shell
oc apply -f alert.yaml
```

Now we need to visit our app to increase the counter.

```shell
oc port-forward service/spring-prometheus-demo-service 8080:8080
```

This will allow you to access the app on your machine by visiting [http://localhost:8080](http://localhost:8080). When you go back to Observe you'll find that the counter should be increased. But if you visit you application more than 10 times, you can also find active alert in `Observe -> Alers`! 

## Alert routing

By default, all alerts in OKD/OpenShift are routed by main instance. If you want to enable user-routing - it is described [here](https://docs.okd.io/4.13/monitoring/enabling-alert-routing-for-user-defined-projects.html). After that, you can create your custom routing by following [this](https://docs.okd.io/4.13/monitoring/managing-alerts.html#creating-alert-routing-for-user-defined-projects_managing-alerts) documentation.

