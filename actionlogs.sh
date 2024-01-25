kubectl logs -n turbointegrations $(kubectl get po -n turbointegrations | awk '/action/ {print $1}') $*
