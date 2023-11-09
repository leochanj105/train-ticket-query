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
  "bufio"
  "strings"
)

var nthds int
var nreqs int

var payaddr = "10.10.1.4"
var tripId = "G1234"

var aid, token string
var date string
var pid int
type Result struct{
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

func readBody(readCloser io.ReadCloser) (error) {
    defer readCloser.Close()
    body, err := ioutil.ReadAll(readCloser)
    //fmt.Println(string(body))
    if err != nil {
        return err
    }
    var data bool
    err = json.Unmarshal(body, &data)
    if err != nil {
            fmt.Println(err)
	    return err
    }
    if data {
       return nil
    }
    fmt.Println("err:", string(body))
    return err
}

func now() int64 {
	return time.Now().UnixNano()
}

var wg sync.WaitGroup
func pay(res []Result, alloids []string, idx int){
  client := httpClient()
  var start, end int64
  for i:=0; i < nreqs;i++{
	//fmt.Println(idx, nthds, i, idx*nthds +i)
	oid := alloids[idx * nreqs + i]
	//fmt.Printf("%d, %d paying for %s\n", pid, idx, oid)
	jsonstr := fmt.Sprintf(`{"tripId":"%s",
                                 "orderId":"%s"}`, tripId, oid)
	fulladdr := fmt.Sprintf("http://%s:18673/inside_payment/pay", payaddr)
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
        err = readBody(resp.Body)
	//fmt.Println(oid)
        res[i] = Result{start, end}
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
  pid, _ = strconv.Atoi(os.Args[5])
  //fmt.Println("nreqs ", nreqs, pid)
}

func main(){
  readParams()
  date = time.Now().AddDate(0,0,1).Format("2006-01-02")
  //fmt.Println(nthds, nreqs, aid, token, date)
  var alloids []string = make([]string, nthds * nreqs)
  file, err := os.Open("tmp/uids")
  if err != nil {
      fmt.Println(err)
  }
  defer file.Close()

  scanner := bufio.NewScanner(file)
  // optionally, resize scanner's capacity for lines over 64K, see next exampl
  idx := 0
  for scanner.Scan() {
      t := scanner.Text()
      oid := strings.Trim(t, " ")
      //fmt.Println(oid)
      if idx >= nthds*nreqs*pid{
	 alloids[(idx - nthds*nreqs*pid)] = oid
	 //fmt.Println(oid)
      }
      idx += 1
      if idx >= nthds*nreqs*(pid+1) {
	 break
      }
  }
  if err := scanner.Err(); err != nil {
      fmt.Println(err)
  }

  //for i:=0;i<nthds*nreqs;i++{
//	fmt.Println(alloids[i])
  //}
  //if pid < 1000{
//	  return
 // }

  var allresults [][]Result = make([][]Result, nthds)
  for i:=0;i<nthds;i++{
	  var results = make([]Result, nreqs)
	  allresults[i] = results
  }
  for i:=0; i < nthds;i++{
	  wg.Add(1)
	  go pay(allresults[i], alloids ,i)
  }
  wg.Wait()
  for _, ms := range allresults {
	  for _, m := range ms {
		  fmt.Println(m.start, m.end)
	  }
  }
}

