# Intro

Docker compose is a tool which helps with managing some more complicated application. If you don't want to remember all those commands, and jus go as easy as `docker compose up -d` then well... You're in right place! :)

We'll follow an extended version of [python app example created by runnable.com](https://runnable.com/docker/python/docker-compose-with-flask-apps)

First, we need to be in correct directory, so:
```shell
cd compose_flask
```

Docker compose by default looks for file `docker-compose.yml`. It will process all instructions in the file, so lets start it and inspect what is happening:

```shell
docker-compose up -d
```

This will take some time, docker will try to start redis first, as other containers depend on it. After that it'll build our python app.

Finally, you should be able to access your app under [http://localhost:5000](http://localhost:5000)

You can also take a look at redisinsight app which allows to take a look what happens in redis itself. Visit [http://localhost:8001/](http://localhost:8001/) and when asked to add new database use following config:
```
Host: redis # this works, because we've named our redis container as... 'redis'
Port: 6379 # note that this port is not exposed in our docker-compose, hovewer it was exposed in image
Name: redis # This name is used as connection name in redisinsight
```

If you want to take a look at the logs, you can use simple
```shell
docker-compose logs
```

This will print logs from all containers, when using docker you can just run `docker logs composeflask_web_1` to get logs from single container. Remember, that it'll show only logs printed to stdout/stderr from container!

If you need to change code of your application you can just edit `app.py` file and run `docker compose up -d --build` <- this will ensure, that all images will be rebuilded (if needed).

To stop your application: `docker compose stop`

If you want to go further, you can take a look at [Kubernetes](https://kubernetes.io) which is much more powerful than docker compose (and more complicated!). As first step to it, you can convert your docker-compsoe into kubernetes manifests using [kompose](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/):
```shell
curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose
kompose convert -o kubernetes.yaml
```

You can now compare your `docker-compose.yml` with `kubernetes.yaml` :)