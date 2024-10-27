`controller/controller.go` waits until a predefined interval, pulls data from `falco-scraper/aggregator` and `node-exporter-scraper/cleaner.go`, combines them and sends it off to ___

`falco-scraper/webserver.go` defines a single endpoint server to receive syscall metrics from Falco.

`falco-scraper/aggregator` defines a hashmap that aggregates the count of syscalls until a predefined time interval where the hashmap is reset

`node-exporter-scraper/scraper.go` scrapes resource metrics from node-exporter and sends the raw data to `cleaner.go`

`node-exporter-scraper/cleaner.go` cleans the data from `node-exporter`

