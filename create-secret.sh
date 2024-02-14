kubectl create namespace turbointegrations

kubectl create secret generic actionscriptkeys -n turbointegrations \
--from-file=hostkey --from-file=hostkey.pub \
--from-file=turboauthorizedkey --from-file=turboauthorizedkey.pub \
--from-literal=turbouser=administrator --from-literal=turbopass='ta5t1c!' \
--from-literal=dbuser=admin --from-literal=dbpass=adm1nPa55 
