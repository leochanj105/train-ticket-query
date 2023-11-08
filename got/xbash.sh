for i in $(seq 1 1 50); do
	go run client.go &
done
wait < <(jobs -p)
