#!/usr/bin/env bash
set -u

direc=$1
#mint=$2
#maxt=$3
#step=$4
reqpt=$2

loginres=($(python3 login.py))
aid=${loginres[0]}
token=${loginres[1]}

#python3 req.py -1 20 xx $aid $token

#echo "doing for #clients=1"
#dirname="$direc/c1r${reqpt}"
#python3 req.py 1 $reqpt $dirname $aid $token

for i in $(seq 1 1 20)
#while IFS= read -r line;
do	
	python3 req.py 1 $reqpt $direc $aid $token &
done
wait < <(jobs -p)


