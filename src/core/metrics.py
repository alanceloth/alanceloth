from __future__ import annotations

from prometheus_client import Counter, Gauge

scrape_counter = Counter("scrape_runs_total", "Total de execuções de scraping")
scrape_failures = Counter("scrape_failures_total", "Falhas durante a execução do scraping")
cruise_records = Gauge("cruise_records", "Quantidade de registros de cruzeiros no banco")
