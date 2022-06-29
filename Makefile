venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

.PHONY: build run clean

build: venv
	git submodule update --init

run: build
	venv/bin/streamlit run 🏠_Home.py

clean:
	git clean -fxd
