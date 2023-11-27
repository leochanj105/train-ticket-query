package main
import (
  //"bytes"
  "sync"
  "io"
  "io/ioutil"
  //"log"
  "net/http"
  "time"
  "fmt"
)

var nthds int
var nreqs int

func httpClient() *http.Client {
    client := &http.Client{
	Transport: &http.Transport{
	    MaxIdleConnsPerHost: 50000,
	},
        Timeout: 60 * time.Second,
    }

    return client
}

func readBody(readCloser io.ReadCloser) ([]byte, error) {
    defer readCloser.Close()
    body, err := ioutil.ReadAll(readCloser)
    //fmt.Println(string(body))
    if err != nil {
        return nil, err
    }
    return body, nil
}

var wg sync.WaitGroup
func req(j int){
  _ = j
  client := httpClient()
  for i:=0; i < nreqs;i++{
	req, err := http.NewRequest(http.MethodGet, "http://10.10.1.4:12031/welcome", nil)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	//req.Close = true
        resp, err := client.Do(req)
        if err != nil {
            fmt.Println(err.Error())
            return
        }
        _, _ = readBody(resp.Body)
        //fmt.Println("done ", i)
        //time.Sleep(5 * time.Second)
  }
  wg.Done()
}

func main(){
  nthds = 10
  nreqs = 20000
  for i:=0; i < nthds;i++{
	  wg.Add(1)
	  go req(i)
  }
  wg.Wait()

}

