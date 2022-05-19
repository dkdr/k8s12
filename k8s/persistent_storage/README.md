# Intro

By default, data in kubernetes pods is not persistent. But no worries, there is a solution to store data: [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes)

# Deploy

First, we need to take a look if we have any kind of StorageClass on our cluster:

```shell
λ kubectl get storageclass
NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  2d11h
```

In KinD you'll get basic storageclass implementation based on [Rancher local-path](https://github.com/rancher/local-path-provisioner)

Since we have a StorageClass, we can create a PersistentVolumeClaim, thanks to which, our storagelcass will automatically create PersistentVolume. This is useful especially in cloud environments where you don't want to give user credentials to your cloud storage. To create PVC you need to run following command:

```shell
kubectl create namespace storagetest
kubectl config set-context --current --namespace=storagetest
kubectl apply -f pvc.yaml
```

And you should see similar output when you'll try to list your PVCs:

```shell
λ kubectl get pvc
NAME            STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
task-pv-claim   Pending                                      standard       5s
```

This means, that PVC wasn't used. We should change that. To do so, we'll create a deployment which uses PVC:

```shell
kubectl apply -f deployment.yaml
```

Now status of our PVC should change:
```shell
λ kubectl get pvc
NAME            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
task-pv-claim   Bound    pvc-3018e714-e9e8-4171-a957-188d67a3530a   3Gi        RWO            standard       3m47s
```

# PersistentStorage test

Let's create some file in our pod:
```shell
λ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-7cd98dbfd7-4n6gt   1/1     Running   0          62s
λ kubectl exec -it nginx-deployment-7cd98dbfd7-4n6gt -- /bin/bash
root@nginx-deployment-7cd98dbfd7-4n6gt:/# echo "Hello World!" > /usr/share/nginx/html/index.html
```

`/usr/share/nginx/html/` is mounted on our PersistentVolume, so let's create some non-persistent, more pessimistic file. Run following command in your pod:
```shell
root@nginx-deployment-7cd98dbfd7-4n6gt:/# echo "Goodbye World!" > /usr/share/nginx/index.html
```

Now, as mentioned above, we need to say goodbye to our pod. You can take a small break to think about him if you get attached to it.
```shell
λ kubectl delete pod nginx-deployment-7cd98dbfd7-4n6gt
pod "nginx-deployment-7cd98dbfd7-4n6gt" deleted
```

Pod should be recreated by deployment, so let's take a look into the new one:
```shell
λ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-7cd98dbfd7-hpb7n   1/1     Running   0          112s

λ kubectl exec -it nginx-deployment-7cd98dbfd7-hpb7n -- /bin/bash
root@nginx-deployment-7cd98dbfd7-hpb7n:/# cat /usr/share/nginx/html/index.html
Hello World!
root@nginx-deployment-7cd98dbfd7-hpb7n:/# cat /usr/share/nginx/index.html
cat: /usr/share/nginx/index.html: No such file or directory
root@nginx-deployment-7cd98dbfd7-hpb7n:/#
```

As you can see, one of our files is perfectly fine, the other one, well... not really.

## Multiple pods

We created our PVC with `ReadWriteOnce` access mode. So it should be mounted to once to one pod, right? Riiight? 

No.

```shell
λ kubectl scale deployment nginx-deployment --replicas=5
deployment.apps/nginx-deployment scaled

λ kubectl get pods -o wide
NAME                                READY   STATUS    RESTARTS   AGE     IP            NODE                 NOMINATED NODE   READINESS GATES
nginx-deployment-7cd98dbfd7-886p4   1/1     Running   0          56s     10.244.0.52   kind-control-plane   <none>           <none>
nginx-deployment-7cd98dbfd7-c9xdl   1/1     Running   0          56s     10.244.0.54   kind-control-plane   <none>           <none>
nginx-deployment-7cd98dbfd7-fpnd9   1/1     Running   0          56s     10.244.0.53   kind-control-plane   <none>           <none>
nginx-deployment-7cd98dbfd7-hpb7n   1/1     Running   0          5m19s   10.244.0.51   kind-control-plane   <none>           <none>
nginx-deployment-7cd98dbfd7-smbn7   1/1     Running   0          56s     10.244.0.55   kind-control-plane   <none>           <none>
```

As you can see, after scaling our deployment, which creates the same pods, we can still run multiple pods, but all of them needs to be on the same node. As stated in documentation:
```shell
ReadWriteOnce - the volume can be mounted as read-write by a single pod, it can allow multiple pods to access the volume when the pods are running on the same node.
```