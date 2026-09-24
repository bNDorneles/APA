.PHONY: all test benchmark clean

all: test

test:
	python python/test_suite.py
	python python/test_authorial.py

benchmark:
	python python/benchmark.py --trials 3 --plot ../images/benchmark_results.png

clean:
	-find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	-rm -f *.png 2>/dev/null || true
