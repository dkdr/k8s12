# Intro

This will be simple. We'll just grant [built-in cluster role](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles) to our user. 

```shell
kubectl create clusterrolebinding uzyszkodnik-view-binding --clusterrole=view --user=uzyszkodnik
```

You can of course write and deploy YAML file, but hey, we were talking about making our job easier!

And now we just need to test it:
```shell
kubectl get deployments -n kube-system --user=uzyszkodnik
```

This works fine, but did it work without ClusterRolebinding? Let's delete the permissions and check out!

```shell
kubectl delete clusterrolebinding uzyszkodnik-view-binding
kubectl get deployments -n kube-system --user=uzyszkodnik
Error from server (Forbidden): deployments.apps is forbidden: User "uzyszkodnik" cannot list resource "deployments" in API group "apps" in the namespace "kube-system"
```

As you can see - it was not working without those permissions. 

# Bind ClusterRole to namespace

So in above example we granted our user access to view almost all resources in all namespaces. Usually we don't want to do it this way. It will be more useful to describe permission in one place and apply it to user per namespace. And here comes RoleBinding to ClusterRole.

```shell
kubectl create rolebinding uzyszkodnik-view-binding --clusterrole=view --user=uzyszkodnik -n kube-system
```

And once again, our users get access to listing pods in `kube-system` namespace. But in this case - that's the only namespace he's entitled for.