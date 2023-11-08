#!/usr/bin/env bash
set -u

np=$1
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

for i in $(seq 1 1 $np)
#while IFS= read -r line;
do	
	#echo $line
	#dirname="$direc/c${line}r${reqpt}"
	#echo "doing for #clients="$line, $dirname
	python3 req.py 10 $reqpt tt $aid $token &
done



