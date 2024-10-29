package main

import (
	"fmt"
	"strconv"
	"strings"
	"time"
)

func main() {
	// falco_scraper.RegisterEndpoint()
	//node_exporter_scraper.GetMetrics()

	for {
		t := time.Now()
		t.Format(time.RFC3339)
		tstr := t.String()
		secstr := strings.Split(strings.Split(strings.Split(tstr, " ")[1], ":")[2], ".")[0]
		i, err := strconv.ParseInt(secstr, 10, 32)
		if err != nil {
			return
		}
		fmt.Println()
		fmt.Println(secstr+" % "+strconv.FormatInt(x, 10), i%x == 0)
	}
}
