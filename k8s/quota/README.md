# Quota

As a cluster admins, sometimes we want to give to user only part of our precious cluster, or maybe as a developers we want to provide necessary resources to our application. The second one is easy, just specify resources in your pods containers and your job is done. But if as an admin you want your users to be forced to do so, you can use [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/). 

Firstly, lets create a namespace and a simple deployment with no resources. 

```shell
kubectl create namespace quota
kubectl config set-context --current --namespace=quota
kubectl create deployment nginx --image=nginx
```

So far so good, now lets say, that we want to force our users to specify resources, and not only that, but we want them to request no more than 3CPU and 8GB of RAM. To do se, we need to create ResourceQuota. Ald lets check what happened after that.

```shell
kubectl get pods
kubectl create quota my-quota --hard=requests.cpu=3,requests.memory=10G
sleep 10 # Lets give our cluster some time to think about life and stuff
kubectl get pods
```

Well, nothing changed. And that's fine, since ResourceQuota will work on newly created pods. So let's create some by scaling our deployment up.

```shell
kubectl scale deployment nginx --replicas=4
```

Now we can verify what is happening by getting pods, but as you will see, there will be no new pods. If you are not sure what is happening, check kubernetes events!

```shell
kubectl get events
```

You'll get message from kubernetes, that you did not specify resources for your pod. Now comes the time to specify them.

```shell
kubectl patch deployment nginx -p '{"spec": {"template": {"spec":{"containers":[{"name":"nginx","resources": {"requests": {"cpu":1, "memory": "4Gi"}}}]}}}}'
```

Now check what is happening in our cluster:

```shell
kubectl get pods
kubectl get deployments
```

Well, well, well, not all pods were created... You can try to fix it in your way.

# LimitRanges

But what if our cluster users don't want to specify the resources, but we still want to limit them in some way? We can use LimitRange. We can use it also to set maximum size of pod. 

```shell
kubectl apply -f limitrange.yaml -f deployment.yaml
```

Aaaandddd.... it's not working. The deployed pods of course. Once again I ask you to take look at the events and please do the needful to fix this issue.