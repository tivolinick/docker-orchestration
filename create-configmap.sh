kubectl create namespace turbointegrations

kubectl create configmap externalhosts -n turbointegrations \
--from-literal turbo_host='10.188.161.53' \
--from-literal db_host='ndf-db.cluster.local'