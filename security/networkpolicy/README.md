# NetworkPolicy

NetworkPolicy is a simple way to limit traffic to/from your application. Usually all traffic inside cluster is open. In this exercise we'll use examples defined in [ahmetb repo](https://github.com/ahmetb/kubernetes-network-policy-recipes).

# Limit network access to your pod

Let's say, that you have a database, to which you want to connect only from backend pod. To make things much easier our database will be simulated by nginx pod. We'll also create the NetworkPolicy.

**This exercise requires administrative privileges**

```shell
oc run database --image=quay.io/jitesoft/nginx --labels="app=mysql,role=database" --expose --port=80
```

Now verify if you can access the "database" from newly created pod:
```shell
oc run -i --tty np-check --rm --image=k8s.gcr.io/busybox --restart=Never -- wget http://database
```

Seems to be working. Now we'll limit acces to this pod by implementing the NetworkPolicy - only pods with label `role: backend` will be able to acces our "database"

```shell
oc apply -f netpol-1.yaml
```

Verify the access once again:
```shell
oc run -i --tty np-check --rm --image=k8s.gcr.io/busybox --restart=Never -- wget http://database
```

And now, with label!
```shell
oc run -i --tty np-check --rm --image=k8s.gcr.io/busybox --restart=Never --labels="role=backend" -- wget http://database
```