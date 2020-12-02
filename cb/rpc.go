package coinbase

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

var basePath string = os.Getenv("GOPATH")

type rpc struct {
	auth Authenticator
	mock bool
}

func (r rpc) Request(method string, endpoint string, params interface{}, holder interface{}) error {

	jsonParams, err := json.Marshal(params)
	if err != nil {
		return err
	}

	request, err := r.createRequest(method, endpoint, jsonParams)
	if err != nil {
		return err
	}

	// var data []byte

	// if r.mock == true {
	// 	data, err := r.simulateRequest(method, endpoint)
	// } else {
	// 	data, err := r.executeRequest(request)
	// }

	data, err := r.executeRequest(request)
	if err != nil {
		return err
	}

	if err := json.Unmarshal(data, &holder); err != nil {
		return err
	}
	return nil
}

func (r rpc) createRequest(method string, endpoint string, params []byte) (*http.Request, error) {

	path := r.auth.getBaseUrl() + endpoint
	req, err := http.NewRequest(method, path, bytes.NewBuffer(params))
	if err != nil {
		return nil, err
	}

	// Authenticate Request

	r.auth.authenticate(req, endpoint, params)

	req.Header.Set("Content-Type", "application/json; charset=utf8")

	return req, nil
}

func (r rpc) executeRequest(req *http.Request) ([]byte, error) {
	resp, err := r.auth.getClient().Do(req)
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()
	buf := new(bytes.Buffer)
	buf.ReadFrom(resp.Body)
	bytes := buf.Bytes()
	if resp.StatusCode != 200 {
		if len(bytes) == 0 {
			log.Println("Response body was empty")
		} else {
			log.Println("Response body: \n \t %s \n", bytes)
		}
		return nil, fmt.Errorf("%s %s failed. Response code was %s", req.Method, req.URL, resp.Status)
	}
	return bytes, nil
}

func (r rpc) simulateRequest(endpoint string, method string) ([]byte, error) {
	fileName := strings.Replace(endpoint, "/", "_", -1)

	filePath := basePath + "/test_data/" + method + "_" + fileName + ".json"

	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		return nil, err
	}
	return data, nil

}
