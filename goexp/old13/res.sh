#!/usr/bin/env bash
set -u
nprocs=$1
nthds=$2
reqpt=$3
dirname=$4
mkdir -p $dirname

loginres=($(python3 ../login.py))
aid=${loginres[0]}
token=${loginres[1]}

#python3 req.py -1 20 xx $aid $token

mkdir -p tmp

echo "reserving..."
#while IFS= read -r line;
for i in $(seq 1 1 $nprocs)
do	
	
	fname="tmp/r$i"
	#echo "doing for #clients="$line, $dirname
	go run gores.go $nthds $reqpt $aid $token > $fname &
done
wait < <(jobs -p)
for i in $(seq 1 1 $nprocs)
do	
	fname="tmp/r$i"
	rname="$dirname/p${nprocs}t${nthds}r${reqpt}_res"
	while IFS=" " read -r oid stt end
	do 
		echo $stt $end >> $rname
	done < $fname
done
wait < <(jobs -p)
