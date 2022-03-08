# Install basic toolset

## Install and configure docker

First we need to open Terminal and install some stuff:

```shell
sudo yum install -y docker  bash-completion vim ca-certificates  # make us a privileged user and install some tools and fresh certificates
sudo update-ca-trust # Update system cert truststore
. /etc/profile.d/bash_completion.sh
```

Next we need to configure our docker to user our registry mirror

```shell
sudo bash -c 'cat <<EOF > /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.<XXXXXXX>.pl"]
}
EOF'
```

`<XXXXXXX>` should be provided on the course. If you're deploying cluster at home, you can probably skip this step

Next, let's add permission for our user to run docker, and make start with our system:
```shell
sudo groupadd docker
sudo usermod -aG docker $USER
sudo systemctl enable docker
```

Our docker is not running right now, so let's try to fix it by turning our VM of and on again:
```shell
sudo reboot
```

This should fix our issue. Truth is, that reboot is needed to reevaluate our user permissions. But "turning it off and on again" to fix some issue is much funnier. 

## Install kind

To provision our basic cluster we'll use [Kubernetes in Docker](https://kind.sigs.k8s.io/).

Let's install it:
```shell
sudo curl -Lo /usr/bin/kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
sudo chmod a+x /usr/bin/kind
```
Commands listed above will download kind binary to /usr/bin/ directory and make it executable for user. We'll do same thing with kubectl binary, which will be used to run commands against our newly created cluster:

## Install kubectl
Kubectl is a CLI interface for our cluster.

```shell
sudo curl -Lo /usr/bin/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo chmod a+x /usr/bin/kubectl
```

## Install octant
Octant is a GUI interface for our cluster.

```shell
sudo rpm -i https://github.com/vmware-tanzu/octant/releases/download/v0.25.1/octant_0.25.1_Linux-64bit.rpm 
```

### Add auto-completion

If you're a lazy person (I hope so, since I'm) you can enable auto-completion in bash:
```shell
source <(kubectl completion bash) 
# add autocomplete permanently to your bash shell
echo "source <(kubectl completion bash)" >> ~/.bashrc
```


Now we're ready to [create cluster](DEPLOY_CLUSTER.md)!