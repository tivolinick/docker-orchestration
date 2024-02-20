
#actionresponse   NodePort   10.233.38.128   <none>        8080:31189/TCP,5000:32000/TCP   5h50m

echo local
curl -vX POST --show-error http://10.233.7.153:5000/status -d '{"actionOid": 123456, "status": "SUCCESS"}' -H  "Content-Type: application/json"
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
echo -----------------------------------------------------------------
echo 5000
curl -vX POST --show-error http://ndf-turbo.cluster.local:5000/status -d '{"actionOid": 123456, "status": "SUCCESS"}' -H  "Content-Type: application/json"
