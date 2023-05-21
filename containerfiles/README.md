# Workshop container image

## Building

Mind the context being the parent directory.

```sh
$ buildah bud -t <image name> ..
```

## Local usage

You can also run the image for local usage. Password is set to `my-password`.

```sh
$ podman run -d -p 8888:8888 --name gozinc notebook:latest start-notebook.sh --NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$JdAN3fe9J45NvK/EPuGCvA$O/tbxglbwRpOFuBNTYrymAEH6370Q2z+eS1eF4GM6Do'
```
