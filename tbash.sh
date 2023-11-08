for i in $(seq 1 1 50); do
#	echo $i &
	python3 welcome.py 5 1000 &
done
wait < <(jobs -p)
