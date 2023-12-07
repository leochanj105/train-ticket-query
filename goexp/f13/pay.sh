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
bash ../orderchange.sh 0

total=$(($nprocs*$nthds*$reqpt))
#echo $total
bash ../deletepay.sh
bash ../queryorder.sh $total 0
python3 ../hex2uuid.py > tmp/uids

fname=tmp/uids
#readarray -t oids < tmp/uids
#python3 req.py -1 20 xx $aid $token

echo "paying..."

for i in $(seq 1 1 $nprocs)
do
	#< pipe_$ai
	pname="tmp/p$i"
	pid=$(($i-1))
	#echo $pid
	go run gopay.go $nthds $reqpt $aid $token $pid > $pname &
done
wait < <(jobs -p)

for i in $(seq 1 1 $nprocs)
do	
	fname="tmp/p$i"
	rname="$dirname/p${nprocs}t${nthds}r${reqpt}_pay"
	while IFS=" " read -r stt end
	do 
		echo $stt $end >> $rname
	done < $fname
done
wait < <(jobs -p)

