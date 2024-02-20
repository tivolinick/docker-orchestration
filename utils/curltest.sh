
#actionresponse   NodePort   10.233.38.128   <none>        8080:31189/TCP,5000:32000/TCP   5h50m

echo local
curl -vX POST --show-error http://10.233.38.128:5000/status -d '{"actionOid": 123456, "status": "SUCCESS"}' -H  "Content-Type: application/json"
echo
echo -----------------------------------------------------------------
echo locahost
curl -vX POST --show-error http://localhost:32000/status -d '{"actionOid": 123456, "status": "SUCCESS"}' -H  "Content-Type: application/json"
echo -----------------------------------------------------------------
echo 127
curl -vX POST --show-error http://127.0.0.1:32000/status -d '{"actionOid": 123456, "status": "SUCCESS"}' -H  "Content-Type: application/json"
echo -----------------------------------------------------------------
echo remote
curl -vX POST --show-error http://ndf-turbo.cluster.local:32000/status -d '{"actionOid": 123456, "status": "SUCCESS"}' -H  "Content-Type: application/json"


#echo =================================================================
#echo TEST APP
#echo local
#curl -vX POST  http://10.233.38.128:8080/status -d '{"actionOid": 123456, "status": "SUCCESS"}' -H  "Content-Type: application/json"
#echo
#echo -----------------------------------------------------------------
#echo remote
#curl -vX POST  http://ndf-turbo.cluster.local:31189/status -d '{"actionOid": 123456, "status": "SUCCESS"}' -H  "Content-Type: application/json"
