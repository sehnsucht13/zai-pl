test:
	python3 -m pytest -v tests/

test-cov:
	python3 -m pytest --cov=zai --cov-config=.coveragerc tests/

lint:
	python3 -m flake8 ./zai

format:
	python3 -m black ./zai ./tests

run:
	python3 -m zai

run_file:
	python3 -m zai ./testfile.zai

freeze:
	pip freeze > requirements.txt

