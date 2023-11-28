#!/usr/bin/env bash
set -u
nprocs=$1
nthds=$2
reqpt=$3
dirname=$4
mkdir -p $dirname
mkdir -p tmp
loginres=($(python3 ../../login.py))
aid=${loginres[0]}
token=${loginres[1]}

bash ../ssoctx.sh

bash ./dbchange.sh 1

total=$(($nprocs*$nthds*$reqpt))

bash querydb.sh $total 1
python3 hex2uuid.py > tmp/uids


fname=tmp/uids

#python3 req.py -1 20 xx $aid $token
echo "canceling..."
for i in $(seq 1 1 $nprocs)
do
	#< pipe_$ai
	pname="tmp/c$i"
	pid=$(($i-1))
	go run gocancel.go $nthds $reqpt $aid $token $pid > $pname&
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

