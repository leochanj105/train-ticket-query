for i in $(seq 1 1 30); do
	go run client.go &
done
wait < <(jobs -p)
