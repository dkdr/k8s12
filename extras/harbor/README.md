# Intro

# WORK IN PROGRESS

In this scenario we'll try to deploy Harbor container registry inside our cluster and use it as our container image source. This scenario is highly depend on how did you provision your cluster. This example will work on Kubernetes in Docker but will need some tweaks on different platforms.

Basically we need to deploy Harbor, create and sign a certificate for it and eventually add our CA cert (with which we signed the certificate) to our nodes. Usually you should do this before/when provisioning a cluster.

## Create certs

Firs we need to create a CA certificate. We'll follow [official Harbor docs](https://goharbor.io/docs/2.1.0/install-config/configure-https/) here. If you need more information about what is happening below, please follow official docs.

```shell
# Create a key
openssl genrsa -out ca.key 4096
# Create CA cert
openssl req -x509 -new -nodes -sha512 -days 3650 \
 -subj "/C=CN/ST=Sosnowiec/L=Sosnowiec/O=example/OU=Personal/CN=harbor.harbor.svc.cluster.local" \
 -key ca.key \
 -out ca.crt
# Create key for Harbor cert
openssl genrsa -out harbor.key 4096
# Prepare CSR
openssl req -sha512 -new \
    -subj "/C=CN/ST=Sosnowiec/L=Sosnowiec/O=example/OU=Personal/CN=harbor.harbor.svc.cluster.local" \
    -key harbor.key \
    -out harbor.csr
# Add additional DNS names for our harbor instance. We'll access it using internal cluster network, so easiest way to do so will be to provide service name, and service+namespace as alt_names
cat > v3.ext <<-EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1=harbor.harbor.svc.cluster.local
DNS.2=harbor.harbor
DNS.3=harbor
EOF

# Sign the cert and add alt_names to it
openssl x509 -req -sha512 -days 3650 \
    -extfile v3.ext \
    -CA ca.crt -CAkey ca.key -CAcreateserial \
    -in harbor.csr \
    -out harbor.crt
```

Now we'll use [script](https://gist.github.com/superbrothers/9bb1b7e00007395dc312e6e35f40931e) provided by @[superbrothers](https://gist.github.com/superbrothers) to add our CA certificates to kind cluster. This is needed because our container runtime needs to accept the CA cert (and all certs signed by it).

```shell
bash kind-load-certificate.sh ca.crt
```

Now we are almost ready to deploy Harbor itself. First we'll create a secret from our cert and key.

```shell
kubectl create namespace harbor
kubectl config set-context --current --namespace=harbor
kubectl create secret tls harbor-tls-secret --cert=harbor.crt --key=harbor.key 
```
```shell
helm install harbor harbor/harbor --set expose.type=clusterIP --set expose.tls.secret.secretName=harbor-tls-secret --set expose.tls.auto.commonName=harbor.harbor.svc.cluster.local
```
