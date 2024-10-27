package falco_scraper

import "fmt"

var aggregatedCalls map[string]int

func updateHashMap(reqBody string) {
	if aggregatedCalls == nil {
		aggregatedCalls = make(map[string]int)
	}
	aggregatedCalls[reqBody]++
	fmt.Println(aggregatedCalls)
}
