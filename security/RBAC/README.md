# Intro

RBAC in kubernetes allows us to grant permission to object to specific users. But what is a user in kubernetes? Well, it depends on your implementation. Kubernetes by itself [doesn't support](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#users-in-kubernetes) LDAP users or anything like that. This is something which is done by Identity Provider, for example [dex](https://dexidp.io/docs/kubernetes/). 

In our case we'll follow examples described on [Magalix blog](https://www.magalix.com/blog/kubernetes-rbac-101).

# Create certificate

First we need to create a certificate which will allow us to connect to our cluster.
```shell
openssl genrsa -out mojcert.key 2048
openssl req -new -key mojcert.key -out mojcert.csr -subj "/CN=uzyszkodnik"
```

Wel'll need to sign that certificate by our kubernetes CA. To do so, we need to copy the certificate from our cluster. As Kubernetes In Docker has limited access to control-plane pods we can copy the certs from our control-plane-node, which in our case is just a docker container
```shell
docker cp kind-control-plane:/etc/kubernetes/pki/ca.key ./
docker cp kind-control-plane:/etc/kubernetes/pki/ca.crt ./
```
If you are wondering "how did we know this?", then there's a hint: Take a look at `kubectl describe pod kube-apiserver-kind-control-plane` - you'll se that apiserver pod is mounting certificates directly from our "master node". 

And sign the cert:
```shell
openssl x509 -req -in mojcert.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out mojcert.crt -days 300
```

Now what we need to do is to add our signed cert and key for this certificate to our `.kubeconfig`:
```shell
kubectl config set-credentials uzyszkodnik  --client-certificate=mojcert.crt --client-key=mojcert.key
kubectl config set-context uzyszkodnik-context --cluster=kind-kind --user=uzyszkodnik
```

Note that in above commands we're not modifying our current context, we're just adding new "user" and context for him.

# Create Role

Now let's compare output from following commands:
```shell
kubectl get pods -n kube-system
kubectl get pods -n kube-system --user=uzyszkodnik
```

As you can see, our user has no access to listing pods. So we need to create a Role for him, and bind this role to user. Take a closer look at [role.yaml](role.yaml) file and apply it to cluster.
```shell
kubectl apply -f role.yaml -n kube-system
```

Now lets try to get pods once again:
```shell
kubectl get pods -n kube-system --user=uzyszkodnik
```

You should be able to get the pods. But that's only possible in `kube-system` namespace. If you want to add more permissions for the user, you'll need to modify the `rules` field in [role.yaml](role.yaml). But considering, that there are a lot of objects with a lot of permissions we can make our work a little easier (and kind of _less secure_) by using build-in roles. Proceed to [CLUSTERROLE.md](CLUSTERROLE.md) 
