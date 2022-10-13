# Intro

Docker allows us to use different type of networks, however usually we'll be using `bridge` type of network - it allows us to run our containers in secure, separate network, where we can easily expose only needed port of selected container.

For full example you can follow [official docs](https://docs.docker.com/network/network-tutorial-standalone/#use-user-defined-bridge-networks). This will be shorter with fever explanations.

To list existing networks you can run:
```shell
$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
93de964f583d        bridge              bridge              local
1186965ad226        host                host                local
d76670cb5a78        none                null                local
```

When creating a simplest container, docker will assign it to default bridge network. You can create simple container by running: `docker run -dit --name alpine1 alpine ash`
To verify which containers are assigned to network, you can run `docker network inspect <network name>`. 

We'll go step further and create our own network, connect some containers to it and verify if network separation works.

No time for, questions, lets go with commands!

```shell
docker network create --driver bridge alpine-net #create new network
docker run -dit --name alpine1 --network alpine-net alpine ash
docker run -dit --name alpine2 --network alpine-net alpine ash
docker run -dit --name alpine3 alpine ash
docker run -dit --name alpine4 --network alpine-net alpine ash
docker network connect bridge alpine4 # We can't create new container in both networks from the beginning, but we can still add more networks to container later.
```

We ran our containers in background (`-d` - detached flag) with interactive (`-i`) TTY (`-t`), running `ash` shell. Because of that, we can easily attach to running container by typing... `docker attach`. So let's verify how our network works. We should be able to communicate between containers in the same network, but not in different networks. As a nice feature - you can use container name to communicate between containers!

Take a look at containers IP addresses - onw of them will have 2 addresses, since it is part of 2 networks:
```shell
$ docker ps -q | xargs -I [] docker inspect -f '{{.Name}}: {{range.NetworkSettings.Networks}}{{.IPAddress}} {{end}}' []
/alpine4: 172.18.0.4 172.17.0.3 
/alpine3: 172.17.0.2 
/alpine2: 172.18.0.3 
/alpine1: 172.18.0.2
```

We'll start with alpine3 - it is connected only to bridge network, so it should not be able to communicate with alpine1:
```shell
$ docker attach alpine3
/ # ping alpine1
ping: bad address 'alpine1'
/ # ping 172.18.0.2
PING 172.18.0.2 (172.18.0.2): 56 data bytes
^C
--- 172.18.0.2 ping statistics ---
4 packets transmitted, 0 packets received, 100% packet loss
/ # ping alpine4
ping: bad address 'alpine4'
/ # ping 172.17.0.3
PING 172.17.0.3 (172.17.0.3): 56 data bytes
64 bytes from 172.17.0.3: seq=0 ttl=64 time=0.428 ms
^C
--- 172.17.0.3 ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
```

As you can see, alpine3 is not very communicative. It is also not able to resolve `alpine4` hostname, but it is still able to talk with it.
To de-attach from container hold CTRL and press `p` then `q`.

```shell
$ docker attach alpine4
/ # ping alpine1
PING alpine1 (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.110 ms
64 bytes from 172.18.0.2: seq=1 ttl=64 time=0.074 ms
64 bytes from 172.18.0.2: seq=2 ttl=64 time=0.082 ms
^C
--- alpine1 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.074/0.088/0.110 ms
/ # ping alpine3
ping: bad address 'alpine3'
/ # ping 172.17.0.2
PING 172.17.0.2 (172.17.0.2): 56 data bytes
64 bytes from 172.17.0.2: seq=0 ttl=64 time=0.260 ms
64 bytes from 172.17.0.2: seq=1 ttl=64 time=0.076 ms
^C
--- 172.17.0.2 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.076/0.168/0.260 ms
```

Ok, stuff looks' like it's working!

Now clean up after our messing around:

```shell
docker container stop alpine1 alpine2 alpine3 alpine4
docker container rm alpine1 alpine2 alpine3 alpine4
docker network rm alpine-net
```

And let's take a look at [storage](../storage/README.md).