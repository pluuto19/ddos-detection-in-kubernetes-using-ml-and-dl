package falco_scraper

import (
	"encoding/json"
	"net/http"
)

const SERVER_ADDR = ":7744"

type outputFields struct {
	EvtTime     int64  `json:"evt.time"`
	SyscallType string `json:"syscall.type"`
}

type requestBody struct {
	Hostname     string
	Output       string
	OutputFields outputFields `json:"output_fields"`
	Priority     string
	Rule         string
	Source       string
	Tags         []string
	Time         string
}

func falcoWebhook(w http.ResponseWriter, req *http.Request) {
	var newSyscall requestBody
	err := json.NewDecoder(req.Body).Decode(&newSyscall)
	if err != nil {
		// log error
		return
	}
	updateHashMap(newSyscall.OutputFields.SyscallType)
}

func RegisterEndpoint() {
	http.HandleFunc("/agent-service/falco", falcoWebhook)
	err := http.ListenAndServe(SERVER_ADDR, nil)
	if err != nil {
		// perform logging for error
		return
	}
}
