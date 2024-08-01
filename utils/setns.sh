if [ $# == 0 ]; then
    echo '1. turbonomic'
    echo '2. turbointegrations'
    read a
    if [ "$a" != '1' -a "$a" != '2' ] ; then
        echo 'Enter 1 or 2'
        exit 1
    fi
else
    a=$1
fi
if [ "$a" == '1' ] ; then
    ns=turbonomic
elif [ "$a" == '2' ] ; then
    ns=turbointegrations
else
    ns=$a
fi

echo kubectl config set-context --current --namespace=$ns
kubectl config set-context --current --namespace=$ns
