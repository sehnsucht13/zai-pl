test:
	python3 -m pytest -v tests/

test-cov:
	python3 -m pytest -v --cov-report term-missing --cov-config=.coveragerc --cov=zai tests/

run:
	python3 -m zai

run_file:
	python3 -m zai ./testfile.zai

freeze:
	pip freeze > requirements.txt
