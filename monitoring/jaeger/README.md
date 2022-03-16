# Jaeger usage example

# WORK IN PROGRESS

In this tutorial we'll use [Jaeger Helm](https://github.com/jaegertracing/helm-charts/tree/main/charts/jaeger) package to deploy simple jaeger instance and some example app. For more production ready deployment take a look at [Jaeger Operator](https://www.jaegertracing.io/docs/1.31/operator/) deployment.

## Install stuff

In this case deploying jaeger and demo app is done by one Helm Chart. So let's do the needful.

Create the namespace and set it as current-context:

```shell
kubectl create namespace tracing
kubectl config set-context --current --namespace=tracing
```

Add the repo:
```shell
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
```

In following command we'll modify some values to deploy also our example app for test the demo scenario.

```shell
helm install jaeger jaegertracing/jaeger --set hotrod.enabled=true  --set provisionDataStore.cassandra=false --set allInOne.enabled=true --set storage.type=none --set agent.enabled=false --set collector.enabled=false --set query.enabled=false 
```


## Cleanup

We'll just simply remove the namespace:

```shell
kubectl delete namespace tracing
```