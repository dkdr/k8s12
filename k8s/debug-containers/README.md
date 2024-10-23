# Debug containers

Based on [this](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container-example) documentation.

To debug our containers we can try to take a look on kubernetes events, od pod logs. But what can we do if our containers does not have any tools in it? We can use debug containers to add those tools.

Let's deploy our container with minimal image
```shell
kubectl create namespace debugcontainers
kubectl config set-context --current --namespace=debugcontainers
kubectl run ephemeral-demo --image=registry.k8s.io/pause:3.1 --restart=Never
```

Our container should be running after a while, so we can try to run shell inside it:
```shell
kubectl get pod ephemeral-demo -o wide
kubectl exec -it ephemeral-demo -- sh
```

And it does not work, as there is no `/bin/sh` in this container. But we have shell in `busybox` image. 
```shell
kubectl debug -it ephemeral-demo --image=busybox:1.28 --target=ephemeral-demo
```

You can run `ifconfig eth0` command to verify that your indeed inside the `ephemeral-demo` container (the IP address should match one printed by `kubectl get pod ephemeral-demo -o wide`). Of course, you can change `busybox` image to any other image with different toolset.

# Copy container

In some cases you want to run a copy of your container, but you need to change it init command. No problem here.
Create a new pod which will be failing (so it will finish it's live by ending main process with exitcode!=0)
```shell
kubectl run --image=busybox:1.28 myapp -- false
```

Now all we have to do is to specify the name of the container and specify the command (note that in below command we do not specify container image, we're just copying existing `myapp` pod)

```shell
kubectl debug myapp -it --copy-to=myapp-debug --container=myapp -- sh
```

We'll be greeted by command prompt and well, we can continue to debug our application, but here we really don't have any, so it's time to finish this exercise.

## Cleanup 
```shell
kubectl delete namespace debugcontainers
```

