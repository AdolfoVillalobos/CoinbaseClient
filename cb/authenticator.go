package coinbase

import "net/http"

type Authenticator interface {
	getBaseUrl() string
	getClient() *http.Client
	authenticate(req *http.Request, endpoint string, params []byte) error
}
