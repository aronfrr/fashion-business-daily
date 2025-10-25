.PHONY: update test

update:
	python -m fashion_business_daily.cli --output data

test:
	pytest
