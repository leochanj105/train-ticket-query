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
echo "canceling..."
for i in $(seq 1 1 $nprocs)
do
	#< pipe_$ai
	fname="tmp/r$i"
	pname="tmp/c$i"
	go run gocancel.go $nthds $reqpt $aid $token $fname > $pname&
done
wait < <(jobs -p)
for i in $(seq 1 1 $nprocs)
do	
	fname="tmp/c$i"
	rname="$dirname/p${nprocs}t${nthds}r${reqpt}_cancel"
	while IFS=" " read -r stt end
	do 
		echo $stt $end >> $rname
	done < $fname
done
wait < <(jobs -p)

