package main
import (
  //"bytes"
  "sync"
  "io"
  "io/ioutil"
  //"log"
  "bytes"
  "net/http"
  "time"
  "fmt"
  "os"
  "strconv"
  "encoding/json"
)

var nthds int
var nreqs int

var resaddr = "10.10.1.4"
var tripId = "G1234"

var aid, token string
var date string

type Result struct{
	oid string
	start int64
	end int64
}

func httpClient() *http.Client {
    client := &http.Client{
	Transport: &http.Transport{
	    MaxIdleConnsPerHost: 50000,
	},
        Timeout: 30 * time.Second,
    }

    return client
}

func readBody(readCloser io.ReadCloser) (string, error) {
    defer readCloser.Close()
    body, err := ioutil.ReadAll(readCloser)
    //fmt.Println(string(body))
    if err != nil {
        return "", err
    }
    data := make(map[string]interface{})
    err = json.Unmarshal(body, &data)
    if err != nil {
            fmt.Println(err)
	    return "", err
    }
    if order, ok := data["order"].(map[string]interface{}); ok {
	var oid string
	if oid, ok = order["id"].(string); ok{
		return oid, nil
        } else{
		fmt.Println("getting oid failed")
		return "", nil
	}
	return oid, err
    } else {
        fmt.Println("wrong type")
    }
    return "", nil
}

func now() int64 {
	return time.Now().UnixNano()
}

var wg sync.WaitGroup
func reserve(res []Result){
  jsonstr := fmt.Sprintf(`{"contactsId":"aded7dc5-06a7-4503-8e21-b7cad7a1f386",
                           "tripId":"%s",
                           "SeatType":2,
                           "date": "%s",
                           "from":"Su Zhou",
                           "to":"Shang Hai"}`, tripId, date)
  client := httpClient()
  var start, end int64
  for i:=0; i < nreqs;i++{
	fulladdr := fmt.Sprintf("http://%s:14568/preserve", resaddr)
	req, err := http.NewRequest(http.MethodPost, fulladdr, bytes.NewBuffer([]byte(jsonstr)))
	req.Header.Set("Cookie", fmt.Sprintf("loginId=%s; loginToken=%s", aid, token))
	req.Header.Set("Content-Type", "application/json")
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	//req.Close = true
        start = now()
        resp, err := client.Do(req)
        end = now()
	lat := end-start
	_ = lat
        if err != nil {
            fmt.Println(err.Error())
            return
        }
        oid, err := readBody(resp.Body)
	//fmt.Println(oid)
        res[i] = Result{oid, start, end}
        //fmt.Println("done ", i)
        //time.Sleep(5 * time.Second)
  }
  wg.Done()
}


func readParams(){
  nthds, _ = strconv.Atoi(os.Args[1])
  nreqs, _ = strconv.Atoi(os.Args[2])
  aid = os.Args[3]
  token = os.Args[4]
}

func main(){
  //nthds = 10
  //nreqs = 100
  readParams()
  date = time.Now().AddDate(0,0,1).Format("2006-01-02")
  //fmt.Println(nthds, nreqs, aid, token, date)
  var allresults [][]Result = make([][]Result, nthds)
  for i:=0;i<nthds;i++{
	  var results = make([]Result, nreqs)
	  allresults[i] = results
  }
  for i:=0; i < nthds;i++{
	  wg.Add(1)
	  go reserve(allresults[i])
  }
  wg.Wait()
  for _, ms := range allresults {
	  for _, m := range ms {
		  fmt.Println(m.oid, m.start, m.end)
	  }
  }
  //wg.Wait()

}

