package node_exporter_scraper

import (
	"bufio"
	"errors"
	"strconv"
	"strings"
)

var resourceMetricsName map[string]float64
var deviceBasedResourceMetrics []string
var noDeviceBasedResourceMetrics []string

func cleanResponseBody(metricsStr string) {
	deviceBasedResourceMetrics = []string{"node_cpu_seconds_total", "node_filesystem_avail_bytes", "node_filesystem_size_bytes", "node_disk_read_bytes_total", "node_disk_written_bytes_total", "node_network_receive_bytes_total", "node_network_receive_drop_total", "node_network_receive_errs_total", "node_network_transmit_packets_total"}
	noDeviceBasedResourceMetrics = []string{"node_vmstat_pgmajfault", "node_memory_MemAvailable_bytes", "node_memory_MemTotal_bytes", "node_forks_total", "node_intr_total", "node_load1", "node_load5", "node_load15", "node_sockstat_TCP_alloc", "node_sockstat_TCP_inuse", "node_sockstat_TCP_mem", "node_sockstat_TCP_mem_bytes", "node_sockstat_UDP_inuse", "node_sockstat_UDP_mem", "node_sockstat_sockets_used", "node_netstat_Tcp_CurrEstab", "node_filefd_allocated"}

	if resourceMetricsName == nil {
		resourceMetricsName = make(map[string]float64)
	}

	for _, noDeviceMetric := range noDeviceBasedResourceMetrics {
		metricValue, err := findMetricValueNoDevice(metricsStr, noDeviceMetric)
		if err != nil {
			continue
		}
		resourceMetricsName[noDeviceMetric] = metricValue
	}

	for _, deviceMetric := range deviceBasedResourceMetrics {
		metricValue, err := findMetricValueDevice(metricsStr, deviceMetric)
		if err != nil {
			continue
		}
		resourceMetricsName[deviceMetric] = metricValue
	}
}

func findMetricValueNoDevice(metricsStr, metric string) (float64, error) {
	scanner := bufio.NewScanner(strings.NewReader(metricsStr))
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "#") || strings.TrimSpace(line) == "" {
			continue
		}
		if strings.HasPrefix(line, metric+" ") {
			parts := strings.Fields(line)
			if len(parts) >= 2 {
				return strconv.ParseFloat(parts[1], 64)
			}
		}
	}
	return 0, errors.New("metric not found")
}

func findMetricValueDevice(metricsStr, metric string) (float64, error) {
	scanner := bufio.NewScanner(strings.NewReader(metricsStr))
	var total float64 = 0

	if metric == "node_cpu_seconds_total" {
		for scanner.Scan() {
			line := scanner.Text()

			if strings.HasPrefix(line, "#") || strings.TrimSpace(line) == "" {
				continue
			}

			if strings.HasPrefix(line, metric) && strings.Contains(line, "mode=\"idle\"") {
				parts := strings.Fields(line)
				if len(parts) >= 2 {
					value, err := strconv.ParseFloat(parts[1], 64)

					if err != nil {
						continue
					}

					total += value
				}
			}
		}
	} else {
		for scanner.Scan() {
			line := scanner.Text()

			if strings.HasPrefix(line, "#") || strings.TrimSpace(line) == "" {
				continue
			}
			if strings.HasPrefix(line, metric) {
				parts := strings.Fields(line)
				if len(parts) >= 2 {
					value, err := strconv.ParseFloat(parts[1], 64)
					if err != nil {
						continue
					}
					total += value
				}
			}
		}
	}

	return total, nil
}

func GetResourceMetrics() *map[string]float64 {
	return &resourceMetricsName
}

func ResetResourceMetrics() {
	resourceMetricsName = make(map[string]float64)
}

/*
IMPROVEMENT
Create a function to eliminate repeated code
*/
