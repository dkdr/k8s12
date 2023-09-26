# Intro

In this example we'll follow [official documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/).

# HPA

Next lets create our deployment

```shell
oc apply -f php-apache.yaml
```

And crate HPA object:
```shell
oc autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
```

All we need to do is create some load in separate terminal:
```shell
oc run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```

Now lets just watch our pods being scaled up and down (when we stop the `kubectl run` process):
```shell
λ oc get hpa php-apache --watch
NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache   55%/50%   1         10        7          10m
```

