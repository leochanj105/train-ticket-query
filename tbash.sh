for i in $(seq 1 1 3000); do
#	echo $i &
	python3 welcome.py 1 1000 &
done
wait < <(jobs -p)
