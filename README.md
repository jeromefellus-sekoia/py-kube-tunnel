# py-kube-tunnel

A small script that opens a full-duplex TCP tunnel from a local port to a remote host via a kubernetes pod, using only plain dependency-free python in the pod.

The script itself mostly behaves as `ssh -L local_port:remote_host:remote_port some_gateway` where some_gateway would be a k8s pod instead

### USAGE

````
./proxy [kube_options...] <POD_NAME> [LOCAL_PORT:]REMOTE_HOST:REMOTE_PORT
````
