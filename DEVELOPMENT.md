# MAT Development

## Environment setup

Clone this repository and initialize your python env

```bash
git clone https://github.com/DiganmeGiovanni/Mat.git
cd Mat

# Initialize python virtual env through pyenv
pyenv virtualenv 3.7.7 mat
pyenv local mat

# Install development requirements
pip install -r requirements-dev.txt
```

Point your IDE interpreter to your new virtualenv and you're good to go!

## Unit testing setup

*TODO*

## Install to test on your local machine

1. Update version number in `setup.py` file
2. Create sources distribution with `python setup.py sdist`
3. Install generated tar through `pip install dist/mat-<version>.tar.gz`, replace `<version>` with the version generated during setup 2
4. You should be ready to use `mat` inside your vitualenv

If you're using `pyenv` and want to test `mat` out of your development folder you can open another shell, navigate to desired folder and use `pyenv shell <environment>` command to activate temporally a specific env for that shell session

> Note: For some reason I experienced some failures during first attempt, solution was to close shell session and start a new one

## Release new version

1. Update version number in `setup.py` file
2. Create sources distribution with `python setup.py sdist`
3. Upload through `twine upload dist/mat-<version>.tar.gz`
