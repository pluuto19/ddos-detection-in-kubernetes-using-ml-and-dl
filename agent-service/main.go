package main

import (
	"agent-service/controller"
	falcoscraper "agent-service/falco-scraper"
)

func main() {
	go falcoscraper.RegisterEndpoint()
	go controller.FetchAndCombine()
	select {}
}
