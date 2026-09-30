.PHONY: help serve pdf figures

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

serve: ## Serve the slides at http://localhost:8000 (no npm install needed)
	cd slides-jp && python3 -m http.server 8000

pdf: ## Export the slides to slides-jp/slides-jp.pdf (needs decktape)
	$(MAKE) -C slides-jp slides-jp

figures: ## Redraw the physics figures from docs/data (needs numpy and matplotlib)
	python3 scripts/plot_physics.py
