test:
	python3 -m pytest -v

run:
	python3 -m zai

run_file:
	python3 -m zai ./testfile.yapl

freeze:
	pip freeze > requirements.txt
