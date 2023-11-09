echo "warmup"
nreqs=$1
dname=$2

bash pay.sh 30 30 10 wup < /dev/null
while IFS=" " read -r nprocs nthds;
do
        #dirname="$direc/c${line}r${reqpt}"
        echo "doing for "$nprocs, $nthds
        bash pay.sh $nprocs $nthds $nreqs $dname < /dev/null
	echo "done"
done

