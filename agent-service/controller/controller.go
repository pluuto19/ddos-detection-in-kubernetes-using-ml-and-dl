package controller

import (
	falcoscraper "agent-service/falco-scraper"
	nodeexporterscraper "agent-service/node-exporter-scraper"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"
	"strings"
	"time"
)

const (
	TIME_INTERVAL       = int64(4)
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
				time.Sleep(time.Second * time.Duration(TIME_INTERVAL))

				syscalls := falcoscraper.GetSyscalls()
				nodeexporterscraper.GetMetrics()
				resourceMetrics := nodeexporterscraper.GetResourceMetrics()

				combinedData := &CombinedMetrics{
					Timestamp:       time.Now().UTC().Format(time.RFC3339),
					Syscalls:        *syscalls,
					ResourceMetrics: *resourceMetrics,
				}

				fmt.Println(combinedData)
				sendToCentralServer(combinedData)

				falcoscraper.ResetSyscalls()
				nodeexporterscraper.ResetResourceMetrics()
			}
		}
	}
}
