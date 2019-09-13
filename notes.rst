create pkg:
python setup.py sdist

upload to pypi:
twine upload dist/*
