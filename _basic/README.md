# Install basic toolset

## Install and configure docker

First we need to open Terminal and install some stuff:

```shell
sudo su -  # make us a priviledged user
yum install -y docker  bash-completion vim ca-certificates # Install some tools and fresh certificates
update-ca-trust # Update system cert truststore
. /etc/profile.d/bash_completion.sh
```

Next we need to configure our docker to user our registry mirror

```shell
cat <<EOF > /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.<XXXXXXX>.pl"]
}
EOF
```

`<XXXXXXX>` should be provided on the course. If you're deploying cluster at home, you can probably skip this step

Next, let's start our docker daemon, and make start with our system:
```shell
service docker start
systemctl enable docker
```

## Install kind

To provision our basic cluster we'll use [Kubernetes in Docker](https://kind.sigs.k8s.io/).

Let's install it:
```shell
curl -Lo /usr/bin/kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
chmod u+x /usr/bin/kind
```
Commands listed above will download kind binary to /usr/bin/ directory and make it executable for user. We'll do same thing with kubectl binary, which will be used to run commands against our newly created cluster:

## Install kubectl

```shell
curl -Lo /usr/bin/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod u+x /usr/bin/kubectl
```

### Add auto-completion

If you're a lazy person (I hope so, since I'm) you can enable auto-completion in bash:
```shell
source <(kubectl completion bash) 
# add autocomplete permanently to your bash shell
echo "source <(kubectl completion bash)" >> ~/.bashrc
```


Now we're ready to [create cluster](DEPLOY_CLUSTER.md)!