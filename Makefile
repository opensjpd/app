venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

.PHONY: build run clean test

build: venv
	git submodule update --init

run: build
	venv/bin/streamlit run 🏠_Home.py

clean:
	git clean -fxd

test:
	docker compose -f test/docker-compose.yaml up --build --exit-code-from controller
