package coinbase

import "strconv"

type Client struct {
	rpc rpc
}

func ApiKeyClient(key string, secret string) Client {
	c := Client{
		rpc: rpc{
			auth: NewApiKeyAuth(key, secret),
			mock: false,
		},
	}
	return c
}

// Get sends a GET request and marshals response data into holder
func (c Client) Get(path string, params interface{}, holder interface{}) error {
	return c.rpc.Request("GET", path, params, &holder)
}

func (c Client) GetBalance() (float64, error) {
	balance := map[string]string{}
	if err := c.Get("account/balance", nil, &balance); err != nil {
		return 0.0, err
	}
	balanceFloat, err := strconv.ParseFloat(balance["amount"], 64)
	if err != nil {
		return 0, err
	}
	return balanceFloat, nil
}
