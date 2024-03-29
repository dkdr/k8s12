# Intro

In this exercise we'll try to pass some parameters to our app. To do so, we'll use [Configmap](https://kubernetes.io/docs/concepts/configuration/configmap/), [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) and [env variables](https://en.wikipedia.org/wiki/Environment_variable). Let's start with the latest and simplest - env vars.

## Env vars
```shell
kubectl create namespace app-config
kubectl config set-context --current --namespace=app-config
kubectl create deployment envvars --image=gcr.io/google-samples/node-hello:1.0 --replicas 2 
```

So we just deployed an app without env variables. Of course, you can specify env variables in Deployment manifest and apply it to cluster. But we'll take some shortcuts here.
```shell
# Add env var do deployment, remember that it'll change pod definition, so it'll create new pods with Rolling deployment strategy.
kubectl set env deployment/envvars MYSUPERVAR=AWESOME_VALUE 
```

Now we'll need to get the pod name, and check whether is sees the env variable, or not.
```shell
λ kubectl get pods
NAME                       READY   STATUS        RESTARTS   AGE
envvars-797cb57b8f-6ktqg   1/1     Terminating   0          93s
envvars-797cb57b8f-gg7kr   1/1     Terminating   0          93s
envvars-84cc747646-8cdkz   1/1     Running       0          5s
envvars-84cc747646-rk8dq   1/1     Running       0          3s
```
Select one of new pods (if you are reading carefully there is a chance, that you'll see only new pods - no worries, that's fine).
```shell
λ kubectl exec -it envvars-84cc747646-8cdkz -- env | grep MYSUPERVAR
MYSUPERVAR=AWESOME_VALUE
```
As you can see, everything worked as expected - variable is available in pod. Let's go further.

## Configmap

Using configmaps to define app config is probably the most popular way to... configure the applications on k8s clusters. In our case we'll simply add files from configmap to our pod, and take a look at how it behaves. We'll take simple example based on [kubernetes docs](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/), you can take a look at other examples which can suit your case better.
```shell
kubectl create configmap konfig --from-file=configmap/
kubectl get configmap konfig -o yaml # Take a look how the data is structured, you can notice, that file names becomes keys of the configmap
kubectl apply -f configmap-deployment.yaml # Create deployment
```

Now lets find the pod and take a look if it really has our files.
```shell
λ kubectl get pods -l app=konfigapp
NAME                         READY   STATUS    RESTARTS   AGE
konfigapp-67f9d57885-n5vfn   1/1     Running   0          5m13s

λ kubectl exec -it konfigapp-67f9d57885-n5vfn -- /bin/bash
root@konfigapp-67f9d57885-n5vfn:/# ls /etc/konfig/
application.properties  somefile.txt
root@konfigapp-67f9d57885-n5vfn:/# cat /etc/konfig/somefile.txt
This is file does nothing important.
It is just existing.
```

Indeed, files are in container. Ok, so let's change ConfigMap, this should also change files in our container. Right? Well, lets check. (But probably you already know the answer). Run below command and make some changes in files.
```shell
λ kubectl edit configmap konfig
configmap/konfig edited
```
In my case I changed content of `somefile.txt` in the ConfigMap to `fdsvfcaiusfvdsyftvctuay`. 
```shell
λ kubectl exec -it konfigapp-67f9d57885-n5vfn -- /bin/bash
root@konfigapp-67f9d57885-n5vfn:/# cat /etc/konfig/somefile.txt
This is file does nothing important.
It is just existing.
```

As you can see, the file in container also changed. This happens only when you're mounting configmap as volume. You can read more about it [here](https://medium.com/@harsh.manvar111/update-configmap-without-restarting-pod-56801dce3388). If you app needs to be restarted when configmap changes, you can use Helm to trigger new deployment when content of configmap changes: [Helm Tips and Tricks](**https://helm.sh/docs/howto/charts_tips_and_tricks/#automatically-roll-deployments**).

## Secrets

Secrets are quite similar to ConfigMaps, however they are a separate object which behaves a little differently. In our example we'll use Secret to store a database password as env variable. If you need more secure way to store Secrets take a look at [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets).

```shell
# First let's create a secret object
kubectl create secret generic credentials --from-literal=username=stronguser --from-literal=password=Str0nGp4ssw0rD
```

Now we just need a pod which will use our secret:
```shell
kubectl apply -f secret-pod.yaml
kubectl get pod secret-env-pod -o yaml
```

You should see, that the variable itself is still not shown in pod definition. This allows to grant permission to getting pod definitions to some users, but if they don't have permissions to get secrets - they can't see its content (unless they can run terminal in pod).



## Cleanup
```shell
kubectl delete namespace app-config
```