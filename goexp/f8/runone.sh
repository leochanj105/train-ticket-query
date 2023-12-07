echo "warmup"
nreqs=$1
dname=$2

bash calc.sh 10 10 100 wup < /dev/null
rm -r wup
while IFS=" " read -r nprocs nthds;
do
        echo "doing for "$nprocs, $nthds
	total=$(($nprocs * $nthds))
	actual=$nreqs
	#if [ $total -lt 101 ]
	#then
#		actual=$(($nreqs * 1))
#		echo $actual
#	fi
	sleep 10
        bash calc.sh $nprocs $nthds $actual $dname < /dev/null
	echo "done"
	rm -r tmp
done

