package controller

import (
	falcoscraper "agent-service/falco-scraper"
	nodeexporterscraper "agent-service/node-exporter-scraper"
	"fmt"
	"strconv"
	"strings"
	"time"
)

const TIME_INTERVAL = int64(4)

func FetchAndCombine() {
	for {
		t := time.Now()
		t.Format(time.RFC3339)
		tStr := t.String()
		secStr := strings.Split(strings.Split(strings.Split(tStr, " ")[1], ":")[2], ".")[0]
		i, err := strconv.ParseInt(secStr, 10, 64)
		if err != nil {
			return
		}
		if i%TIME_INTERVAL == 0 {
			for {
				/*
					Sleep here for x seconds as we have reached a time interval where
					sleeping for x seconds will always wake it up at the next correct
					time of scraping.
				*/
				time.Sleep(time.Second * time.Duration(TIME_INTERVAL))
				syscalls := falcoscraper.GetSyscalls()
				nodeexporterscraper.GetMetrics()
				resourceMetrics := nodeexporterscraper.GetResourceMetrics()

				// combine and send off
				fmt.Println(*syscalls, "\n", *resourceMetrics)
				fmt.Println()

				falcoscraper.ResetSyscalls()
				nodeexporterscraper.ResetResourceMetrics()
			}
		}
	}
}
