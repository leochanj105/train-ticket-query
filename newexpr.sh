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

echo "doing for #clients=1"
dirname="$direc/c1r${reqpt}"
python3 req.py 1 $reqpt $dirname $aid $token

for i in $(seq $mint $step $maxt)
do	
	dirname="$direc/c${i}r${reqpt}"
	echo "doing for #clients="$i, $dirname
	python3 req.py $i $reqpt $dirname $aid $token
done



