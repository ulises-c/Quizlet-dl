.PHONY: install run %

install:
	uv sync
	uv run playwright install firefox

run:
	uv run quizlet-dl.py "$(or $(URL),$(filter-out $@,$(MAKECMDGOALS)))"

%:
	@:
