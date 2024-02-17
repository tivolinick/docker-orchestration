kubectl create namespace turbointegrations

kubectl delete secret actionscriptkeys -n turbointegrations
kubectl create secret generic actionscriptkeys -n turbointegrations \
--from-file=hostkey --from-file=hostkey.pub \
--from-file=turboauthorizedkey --from-file=turboauthorizedkey.pub


kubectl delete secret actionscriptcreds -n turbointegrations
kubectl create secret generic actionscriptcreds -n turbointegrations \
--from-literal=turbouser=administrator --from-literal=turbopass='ta5t1c!' \
--from-literal=dbuser=admin --from-literal=dbpass=adm1nPa55 \
--from-literal=ansibleuser=admin --from-literal=ansiblepass='ta5t1c!'

