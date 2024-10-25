package falco_scraper

import (
	"io"
	"net/http"
)

const SERVER_ADDR = ":7744"

func falcoWebhook(w http.ResponseWriter, req *http.Request) {
	bodyBytes, err := io.ReadAll(req.Body)
	if err != nil {
		// log error
		return
	}
	bodyString := string(bodyBytes)

}

func RegisterEndpoint() {
	http.HandleFunc("/agent-service/falco", falcoWebhook)
	err := http.ListenAndServe(SERVER_ADDR, nil)
	if err != nil {
		// perform logging for error
		return
	}
}
