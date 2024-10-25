`controller/controller.go` combines the data and sends it off to ___

`falco-scraper/webserver.go` defines a single endpoint server to receive syscall metrics.

`falco-scraper/aggregator` defines a hashmap that aggregates the count of syscalls until a predefined time interval and sends it off to `controller`

`node-exporter-scraper/scraper.go` scrapes resource metrics from node-exporter and sends the raw data to `cleaner.go`

`node-exporter-scraper/cleaner.go` cleans the data and sends the data off to `controller`

