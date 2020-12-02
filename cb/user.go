package coinbase

type User struct {
	Id             string   `json:"id,omitempty"`
	Name           string   `json:"name,omitempty"`
	Email          string   `json:"email,omitempty"`
	ReceiveAddress string   `json:"receive_address,omitempty"`
	TimeZone       string   `json:"timezone,omitempty"`
	NativeCurrency string   `json:"native_currency,omitempty"`
	Balance        amount   `json:"balance,omitempty"`
	Merchant       merchant `json:"merchant,omitempty"`
	BuyLevel       int64    `json:"buy_level,omitempty"`
	SellLevel      int64    `json:"sell_level,omitempty"`
	BuyLimit       amount   `json:"buy_limit,omitempty"`
	SellLimit      amount   `json:"sell_limit,omitempty"`
}

type amount struct {
	Amount   string `json:"amount,omitempty"`
	Currency string `json:"currency,omitempty"`
}

type merchant struct {
	CompanyName string `json:"company_name,omitempty"`
	Logo        struct {
		Small  string `json:"small,omitempty"`
		Medium string `json:"medium,omitempty"`
		Url    string `json:"url,omitempty"`
	} `json:"logo,omitempty"`
}
