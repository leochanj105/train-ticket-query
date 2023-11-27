echo "warmup"
nreqs=$1
dname=$2

bash calc.sh 30 30 100 wup < /dev/null
while IFS=" " read -r nprocs nthds;
do
        #dirname="$direc/c${line}r${reqpt}"
        echo "doing for "$nprocs, $nthds
	total=$(($nprocs * $nthds))
	actual=$nreqs
        bash calc.sh $nprocs $nthds $actual $dname < /dev/null
	echo "done"
done

