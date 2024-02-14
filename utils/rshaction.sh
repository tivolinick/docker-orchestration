pod=$(kubectl -n turbointegrations get po |grep actionscript | grep Running | cut -f1 -d' ')
echo $pod
kubectl -n turbointegrations exec --tty --stdin  $pod -- /bin/bash
