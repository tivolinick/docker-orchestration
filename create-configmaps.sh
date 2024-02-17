kubectl create namespace turbointegrations

kubectl delete configmap externalhosts -n turbointegrations 
kubectl create configmap externalhosts -n turbointegrations \
--from-literal turbo_host='10.188.161.53' \
--from-literal db_host='10.188.174.57' \
--from-literal ansible_host='10.188.174.35' \
--from-literal db_port='2345'

kubectl delete configmap actionscriptrefs -n turbointegrations 
kubectl create configmap actionscriptrefs -n turbointegrations \
--from-literal startup='17' \
--from-literal shutdown='17'