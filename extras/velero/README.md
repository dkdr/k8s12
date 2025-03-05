# Install minio

Basically we'll run a minio server on our docker machine and publish ports for it to be accessible by our kubernetes apps.
```shell
docker run -d -p 9000:9000 -p 9001:9001 --name minio1 -e "MINIO_ROOT_USER=minioadmin" -e "MINIO_ROOT_PASSWORD=minioadmin" quay.io/minio/minio server /data --console-address ":9001"
```

And create a bucket:
```shell
mc alias set minio http://127.0.0.1:9000 minioadmin minioadmin
mc mb minio/velero
```

# Install velero

Note, that below s3Url is set to interface accessible from our kubernetes cluster.

```
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts/
helm install velero vmware-tanzu/velero --namespace velero --create-namespace --set-file credentials.secretContents.cloud=credentials-velero.txt --set configuration.backupStorageLocation[0].name=minio --set configuration.backupStorageLocation[0].provider=aws --set configuration.backupStorageLocation[0].bucket=velero --set configuration.backupStorageLocation[0].config.s3Url=http://192.168.100.199:9000 --set configuration.backupStorageLocation[0].config.region=minio --set initContainers[0].name=velero-plugin-for-s3 --set initContainers[0].image=velero/velero-plugin-for-aws:v1.10.1 --set initContainers[0].volumeMounts[0].mountPath=/target --set initContainers[0].volumeMounts[0].name=plugins --set configuration.volumeSnapshotLocation[0].name=minio --set configuration.volumeSnapshotLocation[0].provider=aws --set configuration.volumeSnapshotLocation[0].config.region=minio 
```

# ArgoCD

If ArgoCD is not installed then to do so you can run:
```shell
helm repo add argo https://argoproj.github.io/argo-helm
helm install my-argo-cd argo/argo-cd --version 7.8.7 --wait
```

Now we need to deploy our app:
```shell
kubectl apply -f ../../k8s/argo/argocd-yaml/persistent-volume.yaml
```

We also need to change our PV reclaim policy to Retain:
```shell
kubectl patch pv pvc-6b5b54fa-515d-4bb3-bd6a-1ed59440811f -p "{\"spec\":{\"persistentVolumeReclaimPolicy\":\"Retain\"}}"
```

And wait a little... Now we can write something to our PV:
```shell
kubectl exec -n storagetest deployment/nginx-deployment -- bash -c "echo 'Hello World!' > /usr/share/nginx/html/index.html"
kubectl exec -n storagetest deployment/nginx-deployment -- cat /usr/share/nginx/html/index.html
kubectl get pv
```

Now it's time for a backup:
```shell
velero backup create pv-only-backup --include-resources persistentvolumes --storage-location minio --wait
```

And when the backup is complete, we can remove our cluster, deploy a new one, and basically we need to restore the PV firstly, then we can install ArgoCD and restore our app.
```shell
kind delete cluster
kind create cluster
helm install velero vmware-tanzu/velero --namespace velero --create-namespace --set-file credentials.secretContents.cloud=credentials-velero.txt --set configuration.backupStorageLocation[0].name=minio --set configuration.backupStorageLocation[0].provider=aws --set configuration.backupStorageLocation[0].bucket=velero --set configuration.backupStorageLocation[0].config.s3Url=http://192.168.100.199:9000 --set configuration.backupStorageLocation[0].config.region=minio --set initContainers[0].name=velero-plugin-for-s3 --set initContainers[0].image=velero/velero-plugin-for-aws:v1.10.1 --set initContainers[0].volumeMounts[0].mountPath=/target --set initContainers[0].volumeMounts[0].name=plugins --set configuration.volumeSnapshotLocation[0].name=minio --set configuration.volumeSnapshotLocation[0].provider=aws --set configuration.volumeSnapshotLocation[0].config.region=minio 
```

And now it's time to restore data:
```shell
kubectl get pv
velero restore create pv-only-backup --from-backup pv-only-backup --wait 
kubectl get pv
```

And now - restore ArgoCD:
```shell
helm install my-argo-cd argo/argo-cd --version 7.8.7 --wait
kubectl apply -f ../../k8s/argo/argocd-yaml/persistent-volume.yaml
kubectl get pv 
```

And as you can see, the storage is bounded. This works because our PV has claimRef field which defines which PVC can bound to it automatically.