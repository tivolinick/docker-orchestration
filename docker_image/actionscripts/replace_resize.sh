echo "Replace actionscript executed with the following environment." >> /var/log/stdout
env >> /var/log/stdout
cat | jq -r '.' >> /var/log/stdout
