echo "warmup"
nreqs=$1
dname=$2

bash cancel.sh 10 10 100 wup < /dev/null
while IFS=" " read -r nprocs nthds;
do
        echo "doing for "$nprocs, $nthds
	total=$(($nprocs * $nthds))
	actual=$nreqs
	if [ $total -lt 101 ]
	then
		actual=$(($nreqs * 2))
		echo $actual
	fi
	
        bash cancel.sh $nprocs $nthds $actual $dname < /dev/null
	echo "done"
done
