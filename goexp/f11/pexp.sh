echo "warmup"
nreqs=$1
dname=$2

bash pay.sh 30 30 100 wup < /dev/null
while IFS=" " read -r nprocs nthds;
do
        #dirname="$direc/c${line}r${reqpt}"
        echo "doing for "$nprocs, $nthds
	total=$(($nprocs * $nthds))
	actual=$nreqs
	if [ $total -lt 101 ]
	then
		actual=$(($nreqs * 2))
		echo $actual
	fi
	
        bash pay.sh $nprocs $nthds $actual $dname < /dev/null
	echo "done"
done

