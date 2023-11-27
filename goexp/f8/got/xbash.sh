for i in $(seq 1 1 5); do
	go run client.go &
done
wait < <(jobs -p)
