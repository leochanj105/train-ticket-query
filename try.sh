#!/usr/bin/env bash
set -u

direc=$1
#mint=$2
#maxt=$3
#step=$4
reqpt=$2

#loginres=($(python3 login.py))
#aid=${loginres[0]}
#token=${loginres[1]}
aid=4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f
token=5097f7fc-2b01-48c9-b28f-f59b094d9125
#python3 req.py -1 20 xx $aid $token

#echo "doing for #clients=1"
#dirname="$direc/c1r${reqpt}"
#python3 req.py 1 $reqpt $dirname $aid $token

for i in $(seq 1 1 50)
#while IFS= read -r line;
do	
	python3 req.py 1 $reqpt $direc $aid $token &
done
wait < <(jobs -p)


