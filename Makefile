test:
	python3 -m pytest 

run:
	python3 -m yapl

run_file:
	python3 -m yapl ~/test_modules/testfile.yapl

freeze:
	pip freeze > requirements.txt
