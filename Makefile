test:
	python3 -m pytest -v

run:
	python3 -m yapl

run_file:
	python3 -m yapl ./testfile.yapl

freeze:
	pip freeze > requirements.txt
