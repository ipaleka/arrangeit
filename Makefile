init:
	python3 -m pip install -r requirements/linux.txt

test:
	python3 -m pytest

run:
	python3 -m arrangeit