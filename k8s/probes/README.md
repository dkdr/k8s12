# LivenessProbe

LivenessProbe is a probe which will automatically restart our container if it fails.

We'll se it in action in below example:

```shell
oc apply -f liveness.yaml
```

Our example uses `exec` probe to determine if pod is working fine. It will check for file every 5 seconds, however the file will be deleted after 30s. So lets take a look what happens:

```shell
watch -n 10 oc get pods
```

You should see, that after around 1 minute your pod will be restarted. In our example we didn't specify `failureThreshold` so kubernetes used its default value for this parameter which is `3` so we need to wait for about 30s (container config) + 3 (failureThreshold)*5s (periodSeconds) + some time for container to pull and run the image (depends on the cluster, should be ~10s).

After some time you should see that the container was restarted multiple times:
```shell
λ oc get pods
NAME                       READY   STATUS    RESTARTS   AGE
liveness-exec              1/1     Running   5          7m18s
```

## Cleanup

```shell
oc delete pod liveness-exec
```