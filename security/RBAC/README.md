# Intro

RBAC in kubernetes allows us to grant permission to object to specific users. But what is a user in kubernetes? Well, it depends on your implementation. Kubernetes by itself [doesn't support](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#users-in-kubernetes) LDAP users or anything like that. This is something which is done by Identity Provider, for example [dex](https://dexidp.io/docs/kubernetes/). 

In our case we have htpasswd OAuth deployed with already existing users. To access your k8s ClusterAdmin user you need to log in once again, this time add `-adm` suffix to your username. Password is the same.
```shell
oc login https://oc-api-endpoint -u oc_username-adm
```

# Allow anyuid

You're here because your apache does not want to work, so lets do something a bit "not recommended"...

```shell
λ oc adm policy add-scc-to-user anyuid -z default -n <your_namespace>
```

This allows default serviceAccount to run pods with any user id. In our case - `0`. To make it work, we need to remove existing pod:

```shell
oc delete pod php-apache-74588c5d9c-x8zjg
pod "php-apache-74588c5d9c-x8zjg" deleted
```

Now you can go back to [../k8s/hpa/README.md](../k8s/hpa/README.md)

# Allow user read-only access to namespace

Let's try to grant our default user read-only privileges to `default` namespace. First, verify if user has access. As we're using Admin user - we cas use `--as` flag to run command as other user

```shell
λ oc get pods -n default --as=<our_user>
Error from server (Forbidden): pods is forbidden: User "<our_user>" cannot list resource "pods" in API group "" in the namespace "default"
```

As we can see, it's not possible to view pods as `<our_user>` user in `default` namespace. But we can change that by running:
```shell
λ oc adm policy add-role-to-user view <our_user> -n default
clusterrole.rbac.authorization.k8s.io/view added: "<our_user>"
```

And to verify if that works:
```shell
λ oc get pods -n default --as=<our_user>
No resources found in default namespace.
```

Well... there are no pods, but error is different!

