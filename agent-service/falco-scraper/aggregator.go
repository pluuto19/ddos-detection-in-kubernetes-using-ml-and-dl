package falco_scraper

import (
	"fmt"
)

var aggregatedCalls map[string]int

func updateHashMap(reqBody string) {
	if aggregatedCalls == nil {
		aggregatedCalls = make(map[string]int)
	}

	if reqBody != "" {
		aggregatedCalls[reqBody]++
	}

	fmt.Println(aggregatedCalls)
}

func GetHashmap() *map[string]int {
	return &aggregatedCalls
}

func ResetHashmap() {
	aggregatedCalls = make(map[string]int)
}
