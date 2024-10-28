package falco_scraper

var aggregatedCalls map[string]int

func updateHashMap(reqBody string) {
	if aggregatedCalls == nil {
		aggregatedCalls = make(map[string]int)
	}

	if reqBody != "" {
		aggregatedCalls[reqBody]++
	}

}

func GetSyscalls() *map[string]int {
	return &aggregatedCalls
}

func ResetSyscalls() {
	aggregatedCalls = make(map[string]int)
}
