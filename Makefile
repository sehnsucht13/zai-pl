test:
	python3 -m pytest 

run:
	python3 -m yapl

run_file:
	python3 -m yapl ./yapl/testfile.yapl

freeze:
	pip freeze > requirements.txt
