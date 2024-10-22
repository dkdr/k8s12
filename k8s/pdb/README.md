# PDB and Anti Affinity

There are situations where we want to ensure that at least X number of instances of application are running. But there are also situations where we need to do some maintenance with our cluster or nodes. So what we can do with it? Well, we can use PodDisruptionBudget to handle this for us (to ensure the apps are running, not doing maintenance)

We'll start by creating Deployments - both with podAntiAffinity, but only one will have PDB.

```shell
kubectl create namespace pdb
kubectl config set-context --current --namespace=pdb
kubectl apply -f deployments.yaml
sleep 10
kubectl get pods -o wide
```

As you can see, all 3 pods are for each deployment are deployed on separate node. Now we'll create a PDB for one of the deployment.
```shell
kubectl apply -f pdb.yaml
kubectl pdb
```

As you can see we are allowed to make 1 disruption. So lets make one of our nodes unschedulable and drain pods from it (you should do this when taking node offline).
```shell
kubectl cordon kind-worker3
kubectl drain kind-worker3 --ignore-daemonsets
kubectl get nodes
kubectl get pods -o wide
kubectl get pdb
```

As you can see, node names kind-worker3 is unschedulable, we have 2 pods in Pending state (you can check events for more info) and we have 0 disruptions left. So... lest drain another node!

```shell
kubectl cordon kind-worker2
kubectl drain kind-worker2 --ignore-daemonsets
```

And here you'll see that kubernetes doesn't allow your pod to be evicted, so the drain command will run until you'll find place for another pod in your deployment. So in separate terminal we can return `kind-worker3` node to cluster. And after a while you'll se i your first terminal, that `kind-worker2` was successfully drained.

## Cleanup

```shell
kubeclt uncordon kind-worker2
kubectl delete namespace pdb
```