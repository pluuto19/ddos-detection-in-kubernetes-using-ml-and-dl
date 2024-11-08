package controller

import (
	falcoscraper "agent-service/falco-scraper"
	nodeexporterscraper "agent-service/node-exporter-scraper"
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"sync"
	"time"
)

const (
	TIME_INTERVAL       = int64(4)
	CENTRAL_SERVER_ADDR = "http://localhost:7744/monitor/agent-service"
	CSV_DIR             = "/home/pluuto19/Desktop/metrics_data"
)

type CombinedMetrics struct {
	Timestamp       string             `json:"timestamp"`
	Syscalls        map[string]int     `json:"syscalls"`
	ResourceMetrics map[string]float64 `json:"resource_metrics"`
}

type CSVWriter struct {
	mu          sync.Mutex
	currentFile *os.File
	csvWriter   *csv.Writer
	headers     []string
	dateStr     string
}

func newCSVWriter() (*CSVWriter, error) {
	if err := os.MkdirAll(CSV_DIR, 0755); err != nil {
		return nil, fmt.Errorf("failed to create directory: %v", err)
	}

	return &CSVWriter{}, nil
}

func (w *CSVWriter) ensureFile() error {
	currentDate := time.Now().Format("2006-01-02")

	w.mu.Lock()
	defer w.mu.Unlock()

	if w.currentFile == nil || w.dateStr != currentDate {
		// Close existing file if open
		if w.currentFile != nil {
			w.csvWriter.Flush()
			w.currentFile.Close()
		}

		// Create new file for current date
		filename := filepath.Join(CSV_DIR, fmt.Sprintf("metrics_%s.csv", currentDate))
		file, err := os.OpenFile(filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			return fmt.Errorf("failed to open file: %v", err)
		}

		w.currentFile = file
		w.csvWriter = csv.NewWriter(file)
		w.dateStr = currentDate
	}
	return nil
}

func (w *CSVWriter) writeMetrics(metrics *CombinedMetrics) error {
	if err := w.ensureFile(); err != nil {
		return err
	}

	w.mu.Lock()
	defer w.mu.Unlock()

	// If headers haven't been written yet, write them
	if w.headers == nil {
		headers := []string{"timestamp"}

		// Add syscall headers
		syscallHeaders := make([]string, 0, len(metrics.Syscalls))
		for syscall := range metrics.Syscalls {
			syscallHeaders = append(syscallHeaders, "syscall_"+syscall)
		}
		sort.Strings(syscallHeaders)
		headers = append(headers, syscallHeaders...)

		// Add resource metric headers
		resourceHeaders := make([]string, 0, len(metrics.ResourceMetrics))
		for metric := range metrics.ResourceMetrics {
			resourceHeaders = append(resourceHeaders, "resource_"+metric)
		}
		sort.Strings(resourceHeaders)
		headers = append(headers, resourceHeaders...)

		w.headers = headers
		if err := w.csvWriter.Write(headers); err != nil {
			return fmt.Errorf("failed to write headers: %v", err)
		}
	}

	// Prepare row data
	row := make([]string, len(w.headers))
	row[0] = metrics.Timestamp

	// Fill syscall values
	for syscall, count := range metrics.Syscalls {
		for i, header := range w.headers {
			if header == "syscall_"+syscall {
				row[i] = strconv.Itoa(count)
			}
		}
	}

	// Fill resource metric values
	for metric, value := range metrics.ResourceMetrics {
		for i, header := range w.headers {
			if header == "resource_"+metric {
				row[i] = strconv.FormatFloat(value, 'f', 6, 64)
			}
		}
	}

	// Write row and flush
	if err := w.csvWriter.Write(row); err != nil {
		return fmt.Errorf("failed to write row: %v", err)
	}
	w.csvWriter.Flush()

	return nil
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
	csvWriter, err := newCSVWriter()
	if err != nil {
		fmt.Printf("Error initializing CSV writer: %v\n", err)
		return
	}

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

				if err := csvWriter.writeMetrics(combinedData); err != nil {
					fmt.Printf("Error writing to CSV: %v\n", err)
				}

				fmt.Println(combinedData)
			}
		}
	}
}
