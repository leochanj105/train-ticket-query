#!/usr/bin/env bash
set -u

direc=$1
mint=$2
maxt=$3
step=$4
reqpt=$5

loginres=($(python3 login.py))
aid=${loginres[0]}
token=${loginres[1]}

python3 req.py -1 5 xx $aid $token

#echo "doing for #clients=1"
#python3 req.py 1 $reqpt $direc $aid $token

for i in $(seq $mint $step $maxt)
do	
	echo "doing for #clients="$i
	python3 req.py $i $reqpt $direc $aid $token
done



