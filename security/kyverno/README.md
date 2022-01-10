# Intro

As cluster-administrator you probably have some ideas which you'll want to enforce on the cluster. As remote work becomes a standard it can be hard to punish users. But there are of course some less painful ways to implement policies. [Kyverno](https://kyverno.io) is one way to do this.

We'll use modified version of [kyverno quickstart](https://kyverno.io/docs/introduction/#quick-start)

# Install

We'l start with installing the tool:
```shell
kubectl create namespace kyverno
kubectl config set-context --current --namespace=kyverno
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno --version 2.1.4
```

And lets deplyo the policy:
```shell
kubectl apply -f policy-deployment.yaml
```

Now we'll try to create a pod which will fail our policy.

```shell
kubectl create deployment nginx --image=nginx -n default
```

You should get an error:
```shell
λ kubectl create deployment nginx --image=nginx -n default
error: failed to create deployment: admission webhook "validate.kyverno.svc-fail" denied the request:

resource Deployment/default/nginx was blocked due to the following policies

require-labels:
  autogen-check-for-labels: 'validation error: label ''app.kubernetes.io/nazwa'' is
    required. Rule autogen-check-for-labels failed at path /spec/template/metadata/labels/app.kubernetes.io/nazwa/'
```

Kyverno is smart enough to block creation of objects which are creating Pods. That's why even that you created Deployment, and policy matches Pods, it failed.

So let's try to create a pod which will work:
```shell
kubectl run nginx --image nginx --labels app.kubernetes.io/nazwa=nginx -n default
```

In this example we're running pod directly because of lack of support to add pod labels in `kubectl create deployment` command.

However, you can also try to create bad pod directly:

```shell
kubectl run nginx --image nginx --labels app.kubernetes.io/name=nginx -n default
```

And now it's time to clean up. You don't want to have this policy on your cluster for whole time. 
```shell
kubectl delete clusterpolicy require-labels
```

# Kyverno frontend

You can also deploy a simple frontend for you kyverno installation. This should help others to make their YAML files compliant to your policies.

```shell
helm repo add policy-reporter https://kyverno.github.io/policy-reporter
helm repo update
helm install policy-reporter policy-reporter/policy-reporter --set kyvernoPlugin.enabled=true --set ui.enabled=true --set ui.plugins.kyverno=true -n policy-reporter --create-namespace
```

Now lets change our policy from enforcing to audit. This will allow us to create pods without label, but such things can be reported. This is useful when you want to implement kyverno without making mess with stuff which is already deployed.
Simply edit the [policy-deployment.yaml](policy-deployment.yaml) and change `validationFailureAction: enforce` to `validationFailureAction: audit`.

Now we can access the frontend and take a look at some "bad pods".

```shell
kubectl port-forward service/policy-reporter-ui 8082:8080 -n policy-reporter
```