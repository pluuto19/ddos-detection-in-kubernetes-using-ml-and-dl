package main

import "agent-service/node-exporter-scraper"

func main() {
	// falco_scraper.RegisterEndpoint()
	node_exporter_scraper.GetMetrics()
}
