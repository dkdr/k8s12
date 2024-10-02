# Intro

This time we'll deploy example of logging stack. To do so, we'll need to deploy [FluentBit](https://fluentbit.io/) as our log parser and forwarder, and [syslog-ng](https://github.com/syslog-ng/syslog-ng) as our log receiver (usually you'll use something "bigger" like [OpenSearch](https://opensearch.org/) or [Graylog](https://www.graylog.org/))

# Install software

First, we'll deploy a very simple pod which will forward all http request to its stdout - this will allow us to easily see what logs are send from fluentbit.
```shell
kubectl create deployment http-echo --image=mendhak/http-https-echo --replicas 1
kubectl patch deployment http-echo -p '{"spec": {"template":{"metadata":{"annotations":{"fluentbit.io/exclude":"true"}}}} }'
kubectl expose deployment http-echo --port 8080 --target-port 8080 --type ClusterIP
```

Note, that there is a patch command, which adds specific annotation to pod. `fluentbit.io/exclude":"true"` annotation will force fluent-bit to not send logs from this pod to... this pod. Since all our sent logs will end on http-echo stdout, whose would be also collected by fluent bit and sent to this pod, which would quickly end with a LOT of logs. Since fluent-bit logs requests sent via http, we're doing the same in [fluent-bit-values.yaml](fluent-bit-values.yaml) file. You can read more about this feature in [Fluentbit Documentation](https://docs.fluentbit.io/manual/pipeline/filters/kubernetes#kubernetes-annotations).

So lets deploy our fluentbit:
```shell
helm repo add fluent https://fluent.github.io/helm-charts
helm upgrade --install -f fluent-bit-values.yaml fluent-bit fluent/fluent-bit 
```

Note that in [fluent-bit-values.yaml](fluent-bit-values.yaml)  there is a whole config section which was prepared for this exercise. In most cases you will modify the [OUTPUTS](https://docs.fluentbit.io/manual/pipeline/outputs) section. However take a look at [Kuberenetes filter config](https://docs.fluentbit.io/manual/pipeline/filters/kubernetes).

Since we have everything deployed the last step is to verify if it works (the longer you wait the more logs you'll get!):
```shell
kubectl logs deployment/http-echo
```

With that you should see a lot of json logs send to our http server. Using tools like [OpenSearch](https://opensearch.org/)  could help you work with this type of logs (for example filter logs by specific pods/labels/fields). 