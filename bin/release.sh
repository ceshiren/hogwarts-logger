cd $(dirname $BASH_SOURCE)/../
pwd
rm dist/*
python -m build
unzip -l dist/*.whl
twine upload -r ceba dist/*
twine upload -r pypi dist/*
