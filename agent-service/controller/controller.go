package controller

import (
	falcoscraper "agent-service/falco-scraper"
	nodeexporterscraper "agent-service/node-exporter-scraper"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const (
	TIME_INTERVAL       = int64(1)
	CENTRAL_SERVER_ADDR = "http://localhost:7744/monitor/agent-service"
)

type CombinedMetrics struct {
	Timestamp       string             `json:"timestamp"`
	Syscalls        map[string]int     `json:"syscalls"`
	ResourceMetrics map[string]float64 `json:"resource_metrics"`
}

func sendToCentralServer(data *CombinedMetrics) {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return
	}

	req, err := http.NewRequest("POST", CENTRAL_SERVER_ADDR, bytes.NewBuffer(jsonData))
	if err != nil {
		return
	}

	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return
	}
	defer func(Body io.ReadCloser) {
		err := Body.Close()
		if err != nil {
			return
		}
	}(resp.Body)

	if resp.StatusCode != http.StatusOK {
		return
	}

}

func FetchAndCombine() {
	ticker := time.NewTicker(time.Second * time.Duration(TIME_INTERVAL))
	defer ticker.Stop()

	for {
		now := time.Now()
		if now.Second()%int(TIME_INTERVAL) == 0 {
			for {
				<-ticker.C

				syscalls := falcoscraper.GetSyscalls()
				nodeexporterscraper.GetMetrics()
				resourceMetrics := nodeexporterscraper.GetResourceMetrics()

				if syscalls == nil || resourceMetrics == nil {
					fmt.Println("Warning: Received nil metrics")
					continue
				}

				combinedData := &CombinedMetrics{
					Timestamp:       time.Now().UTC().Format(time.RFC3339),
					Syscalls:        *syscalls,
					ResourceMetrics: *resourceMetrics,
				}

				sendToCentralServer(combinedData)
				falcoscraper.ResetSyscalls()
				fmt.Println(combinedData)
			}
		}
	}
}
