package main

import (
	"fmt"
	"log"
	"os"

	coinbase "./cb"
)

func main() {
	c := coinbase.ApiKeyClient(os.Getenv("COINBASE_KEY"), os.Getenv("COINBASE_SECRET"))

	user := coinbase.User{}

	err := c.Get("/v2/user", nil, &user)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf(user.Name)
}
