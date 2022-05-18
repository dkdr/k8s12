# First docker app

In this exercise you'll build your first docker application, which you'll be able to use as container image to create your first pod.
Examples are based on files provided by [awesome-compose](https://github.com/docker/awesome-compose/tree/master/flask)

## Build the app

To build the app you should in _basic/docker directory and run this command
```shell
docker build -f Dockerfile . -t app:v1
```

This will create a new docker image which can be run as a container. Check the output of `docker images` command to new image.

Take a look at the output of `docker build`. You should see, that all comands were run, and `pip3 install -r requirements.txt --no-cache-dir` step will take some time (usually few seconds).

Now let's change our app code and run the build again. Edit the [app.py](app.py) file and change `Hello World!` to for exmaple `Hello WORD!`. Now run the build again:

```shell
docker build -f Dockerfile . -t app:v2
```

Compare output of first run of `docker build` and the second one. You should see a difference in build time, and output length. This happens because of docker caching the result of first build and making changes only in layers that were modified (and of course in each layer after the modified one).

## Run the app

Now lets try to run our app:
```shell
docker run -d app:v1
```