.PHONY: init install run clean

# Create virtual environment
init:
	python3 -m venv venv
	source venv/bin/activate && pip install --upgrade pip && pip install .

# Activate environment and run your app (optional)
run:
	source venv/bin/activate && GEMINI_API_KEY=$(GEMINI_API_KEY) flask --app Duck_PA run

# Re-install dependencies (optional)
install:
	source venv/bin/activate && pip install .

# Clean environment (optional)
clean:
	rm -rf venv