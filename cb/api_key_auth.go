package coinbase

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"net"
	"net/http"
	"time"

	"./config"
)

type apiKeyAuthenticator struct {
	Key     string
	Secret  string
	BaseURL string
	Client  *http.Client
}

func NewApiKeyAuth(key string, secret string) *apiKeyAuthenticator {
	a := &apiKeyAuthenticator{
		Key:     key,
		Secret:  secret,
		BaseURL: config.BaseURL,
		Client: &http.Client{
			Timeout: time.Minute,
		},
	}
	return a
}

func (a apiKeyAuthenticator) authenticate(req *http.Request, endpoint string, params []byte) error {
	timestamp := fmt.Sprintf("%v", time.Now().Unix())
	var message string
	if req.Method == "GET" {

		message = timestamp + req.Method + endpoint
		fmt.Println(message)

	} else if req.Method == "POST" {
		message = timestamp + req.Method + endpoint + string(params)
	}
	h := hmac.New(sha256.New, []byte(a.Secret))
	h.Write([]byte(message))

	signature := hex.EncodeToString(h.Sum(nil))
	fmt.Println(signature)

	req.Header.Set("CB-ACCESS-KEY", a.Key)
	req.Header.Set("CB-ACCESS-SIGN", signature)
	req.Header.Set("CB-ACCESS-TIMESTAMP", timestamp)

	return nil
}

func (a apiKeyAuthenticator) getBaseUrl() string {
	return a.BaseURL
}

func (a apiKeyAuthenticator) getClient() *http.Client {
	return a.Client
}

func dialTimeout(network, addr string) (net.Conn, error) {
	var timeout = time.Duration(2 * time.Second) //how long to wait when trying to connect to the coinbase
	return net.DialTimeout(network, addr, timeout)
}
