# Work with nodes

In those exercises we'll do some typical stuff when working with nodes and pods.

# Evict node

Sometimes you just need to take the node off the cluster, like when you want to upgrade it manually (most tools can do it automatically). 

To do so, you firstly should make the node as unschedulable, so no new pod will be assigned to it.
```shell
kubectl cordon node kind-worker
```

You can verify if node is unschedulable by running
```shell
kubectl get nodes
```

You should see, that node `kind-worker` has status SchedulingDisabled. But this only means, that no new pod will be assigned to it. We also need to evict the ones which are already running!

```shell
kubeclt drain kind-worker
```

Well... that didn't work... Kubernetes will try to prevent us from doing some nasty stuff, like for example removing pods which are deployed by DaemonSet. But for every case of a problem you'll find a solution right in the error message:
```shell
λ kubectl drain kind-worker
node/kind-worker cordoned
error: unable to drain node "kind-worker" due to error:cannot delete DaemonSet-managed Pods (use --ignore-daemonsets to ignore): kube-system/kindnet-66jx6, kube-system/kube-proxy-wq2kj, monitoring/kube-monitoring-prometheus-node-exporter-lfqrt, continuing command...
There are pending nodes to be drained:
 kind-worker
cannot delete DaemonSet-managed Pods (use --ignore-daemonsets to ignore): kube-system/kindnet-66jx6, kube-system/kube-proxy-wq2kj, monitoring/kube-monitoring-prometheus-node-exporter-lfqrt
```

Well, all you need to do is follow the message :) You should be left only with pods ran by DaemonSets - check the `kubectl describe node kind-worker` command.

# Assign pod to node

First, we'll need to add some label to our node to make it special, one of a kind, irreplaceable...

```shell
kubectl label node kind-worker disktype=ssd
```

Next, you can just deploy a pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/pod-nginx.yaml
```

As you can see, pod has a `nodeSelector` field which specifies what labels should node have to take our pod (remember, that those nodes will still need to have free resources on them to run the pod!)