package controller

import (
	falco_scraper "agent-service/falco-scraper"
	node_exporter_scraper "agent-service/node-exporter-scraper"
	"strconv"
	"strings"
	"time"
)

const TIME_INTERVAL = int64(2)

func FetchAndCombine() {
	for {
		t := time.Now()
		t.Format(time.RFC3339)
		tStr := t.String()
		secStr := strings.Split(strings.Split(strings.Split(tStr, " ")[1], ":")[2], ".")[0]
		i, err := strconv.ParseInt(secStr, 10, 32)
		if err != nil {
			return
		}
		if i%TIME_INTERVAL == 0 {
			syscalls := falco_scraper.GetSyscalls()
			falco_scraper.ResetSyscalls()
			resourceMetrics := node_exporter_scraper.GetResourceMetrics()
			node_exporter_scraper.ResetResourceMetrics()
			// combine and send off
		}
	}
}
