package node_exporter_scraper

import (
	"io"
	"net/http"
)

func GetMetrics() {
	resp, err := http.Get("http://localhost:9100/metrics")
	if err != nil {
		return
	}
	nodeMetricsByte, err1 := io.ReadAll(resp.Body)
	if err1 != nil {
		return
	}

	cleanResponseBody(string(nodeMetricsByte))
}
