kubectl create namespace turbointegrations

kubectl delete secret actionscriptkeys -n turbointegrations
kubectl create secret generic actionscriptkeys -n turbointegrations \
--from-file=hostkey --from-file=hostkey.pub \
--from-file=turboauthorizedkey --from-file=turboauthorizedkey.pub \
--from-literal=turbouser=administrator --from-literal=turbopass='ta5t1c!'


kubectl delete secret actionscriptcreds -n turbointegrations
kubectl create secret generic actionscriptcreds -n turbointegrations \
--from-literal=db_user=admin --from-literal=db_pass=adm1nPa55 \
--from-literal=ansible_user=admin --from-literal=ansible_pass='ta5t1c!'

