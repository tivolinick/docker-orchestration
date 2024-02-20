curl -vX POST --show-error http://ndf-turbo.cluster.local:5000/status -d "{\"actionOid\": \"$1\", \"status\": \"SUCCESS\"}" -H  "Content-Type: application/json"
