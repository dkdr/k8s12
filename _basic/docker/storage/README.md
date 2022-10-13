# Intro

In this exercise we'll learn how to handle data in Docker. By default, when you run a container it creates non-persistent writable layer which allows you to modify whatever you want (with no effect on other containers based on the same image). But in many cases you'll need to persist some data. Here we'll use 2 most popular ways to do it: bind and volume.

# Bind

Let's run commands first, and think later:

```shell
docker run -it --rm -d -p 8080:80 --name web -v ./site-content:/usr/share/nginx/html nginx
```

Now you can try to visit this awesome webpage: [http://localhost:8080](http://localhost:8080). Doesn't it look great?

So what happened under the hood? We run `nginx` image and binded our local `site-content` directory to containers `/usr/share/nginx/html` directory. You can of course make some modifications to index.html file and take a look what happens then.

There is one more interesting thing, `-p 8080:80` parameter which binds our local `8080` port to containers `80` port. Using this command you can for example create a 3 container app - frontend+backend+database and expose only the frontend for users.

# Volume management

Docker recommends usage of volumes - time to check it out.

First - create a test volume:
```shell
docker volume create mydata
```

You can verify, that it was created by running `docker volume ls`. Docker will, by default, put all created volumes in `/var/lib/docker/volumes/` - you can check what happened there: `sudo ls /var/lib/docker/volumes/`

Ok, now let's create some container and mount this dir to it and verify if persistence works as expected:
```shell
docker run --name persistent -itd -v mydata:/var/opt/mydata bash:latest bash
docker exec -it persistent bash
```

Ok, now we created a new container, and also ran an interactive command in it. You can use `docker exec` to run everything which is available inside container. This time we'll just create some files:

```shell
$ docker exec -it persistent bash
bash-5.2# echo "Hello from training!" > /var/opt/mydata/test.txt 
bash-5.2# echo "Goodbye from training!" > /var/opt/test.txt 
```

Now press `Ctrl+D` to exit from terminal. Let's verify if files are still there:
```shell
$ docker exec persistent cat /var/opt/mydata/test.txt
Hello from training!
$ docker exec persistent cat /var/opt/test.txt
Goodbye from training!
```

Ok. So we created one file in directory which was mounted as volume and the second one -in some container directory. Now we'll remove the container, and recreate it the same way we created it at beggining.

```shell
$ docker stop persistent
persistent
$ docker rm persistent
persistent
$ docker run --name persistent -itd -v mydata:/var/opt/mydata bash:latest bash
20e743b71ed0413c64d18d168e32b23652c5c130e9ac924bdaba6c3ff9995a6e
$ docker run --name persistent -itd -v mydata:/var/opt/mydata bash:latest bash
20e743b71ed0413c64d18d168e32b23652c5c130e9ac924bdaba6c3ff9995a6e
$ docker exec persistent cat /var/opt/test.txt
cat: can't open '/var/opt/test.txt': No such file or directory
```

This is useful when for example: you want to run the same application in the same container, but want to limit what can really be changed in log run. Having problem with some app? Just recreate the container, mount its data, and you should be fine (unless data is the problem!) :)