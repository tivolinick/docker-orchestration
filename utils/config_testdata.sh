#!/bin/bash
theDir="$(pwd)/$(dirname $0)/.."
dirs='actionscriptcreds actionscriptrefs externalhosts sshkeys'
cd

# actionscriptcreds actionscriptrefs externalhosts sshkeys
while getopts 'lra' o ; do

    case $o in
    l)
        ls $dirs ;;
    r)
        echo remove
        for dir in $dirs ; do
            rm -f $dir/*
        done
        ls $dirs ;;
    a)
        echo add
        # for dir in $dirs ; do
        for line in  $(awk '/create / {dirname=$4} ; /from-literal/ {print dirname"/"$2}' "$theDir/create-configmaps.sh" | \
                    sed 's/--from-literal=//g' | sed "s/'//g") \
            $(awk '/create / {dirname=$5 ; if (dirname=="actionscriptkeys") {dirname="sshkeys"}} ; /from-literal/ {print dirname"/"$1,dirname"/"$2}' "$theDir/create-secrets.sh"  | \
                    sed 's/--from-literal=//g' | sed "s/'//g")
        do
            echo $line
            echo $line | cut -f2 -d '=' > $(echo $line | cut -f1 -d'=')
            
        done
        ls $dirs ;;
    ?)
        echo oops ;;    
    esac
done