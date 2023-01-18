# Intro

In this exercise we'll deploy [pint](https://cloudflare.github.io/pint/) which is a prometheus rule linter created by [Cloudflare](https://www.cloudflare.com/). This tool is different from [promtool](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/) since it is able to verify thing, like existence of metrics used in alert in Prometheus. This tool is not released as stable version, so keep in mind, that many thins can be changed in new version.

We'll use helm chart created in this repo to deploy the pint instance. It'll mount configmaps created by prometheus operator and verify that prometheus deployed by kube-prometheus-stack has all the metrics.

Pint can also be used in lint or CI mode, which in many cases can be a better solution, since pint allows you to specify exclusions for some rules as comments in YAML. Those comments are not stored in kubernetes API when you are creating PrometheusRule object, so in some cases it might be better to use lint mode outside of cluster.

Enough talking, lets deploy this bad boy.

```shell
helm upgrade --install -f values.yaml --namespace monitoring pint ./ 
```

Keep in mind, that you need to deploy pint in the same namespace as prometheus, since it will use ConfigMaps created by prometheus operator.

Next, take a look at you prometheus instance and verify what is returnet by prometheus when you look up `pint_problem` metric. 