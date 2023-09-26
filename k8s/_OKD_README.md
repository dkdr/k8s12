# OKD

## Install oc binary

First, we need to "install" oc binary. 

```shell
wget -O oc.tar.gz https://github.com/okd-project/okd/releases/download/4.13.0-0.okd-2023-09-03-082426/openshift-client-linux-4.13.0-0.okd-2023-09-03-082426.tar.gz
tar xvf oc.tar.gz
rm oc.tar.gz
sudo mv oc /usr/bin/
sudo chmod u+x /usr/bin/oc
```

## Access the cluster

To access the cluster we'll need to perform `oc login` command. This does not exist in standard kubectl binary. Credentials needed to access the cluster will be provided on training.
```shell
oc login https://oc-api-endpoint -u oc_username
oc project oc_username
```