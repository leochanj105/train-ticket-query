echo "warmup"
nreqs=$1
dname=$2

bash cancel.sh 10 20 100 wup < /dev/null
rm -r wup
while IFS=" " read -r nprocs nthds;
do
        echo "doing for "$nprocs, $nthds
	total=$(($nprocs * $nthds))
	actual=$nreqs
#	if [ $total -lt 101 ]
#	then
	#	actual=$(($nreqs * 2))
#		echo $actual
#	fi
	
        bash cancel.sh $nprocs $nthds $actual $dname < /dev/null
	rm -r tmp
	echo "done"
done

