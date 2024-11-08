package falco_scraper

import "sync"

var (
	aggregatedCalls map[string]int
	mutex           sync.RWMutex
)

func updateHashMap(reqBody string) {
	mutex.Lock()
	defer mutex.Unlock()

	if aggregatedCalls == nil {
		aggregatedCalls = make(map[string]int)
	}

	if reqBody != "" {
		aggregatedCalls[reqBody]++
	}
}

func GetSyscalls() *map[string]int {
	mutex.RLock()
	defer mutex.RUnlock()

	result := make(map[string]int)
	for k, v := range aggregatedCalls {
		result[k] = v
	}
	return &result
}

func ResetSyscalls() {
	mutex.Lock()
	defer mutex.Unlock()
	aggregatedCalls = make(map[string]int)
}
