kubectl logs $(kubectl get po | awk '/rsys/ {print $1}') $*
