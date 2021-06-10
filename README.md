## Google Cloud Run PyPi registry

This repo contains code to build and deploy a PyPi registry to Google Cloud Run.

This project is an early stage proof of concept for how a private registry can be easily deployed and updated using Github Actions.

### How to build a package
Based on instructions from [here](https://docs.gitlab.com/ee/user/packages/pypi_repository/#install-pip-and-twine)

See `packages/gcp_util` for an example of how to write `__init__.py` and `setup.py`

```
mkdir packages/my_new_package
cd packages/my_new_package
touch __init__.py setup.py <your_file_name>.py
# add your code  to <your_file_name>.py
# import your modules in __init__.py
# fill in your setup.py
python3 setup.py sdist bdist_wheel
```

Example `setup.py`
```buildoutcfg
import setuptools

setuptools.setup(
    name="gcp-util", # make sure to use dash and not underscore
    version="0.0.3",
    packages=setuptools.find_packages(),
    # install_requires can be ignore if you do not have any external dependencies
    install_requires=[
          'google-cloud-pubsub',
      ],
    python_requires='>=3.6',
    # optional attributes
    author="Conall Daly",
    author_email="conalldalydev@gmail.com",
    description="Google Cloud Platform Utility Package",
    url='https://github.com/tunnelWithAC/gcp-cloud-run-pypi/tree/master/packages/gcp_util',
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
```

WIP: add Github Action for building and publishing package
[source](https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions#publishing-to-package-registries)

```
# This workflow will upload a Python Package using Twine when a release is created
name: Upload Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install setuptools wheel twine
      - name: Build and publish
        env:
          TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
          TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
        run: |
          python setup.py sdist bdist_wheel
          twine upload dist/*
       
       # twine upload will be replaced gsutil rsync when using compute engine and storage bucket 
       # instead of Cloud Run
          
    #  TODO add this (needs pip install pytest along with actual tests)
    - name: Run tests with pytest
      run: pytest --cov=pubsub_to_bq tests --cov-fail-under=80
```

### Run locally
```
docker build -t pypi .
docker run -p 80:80  --name pypi --rm -it pypi
```

### How to deploy to Google Cloud Run

```
gcloud builds submit --tag "gcr.io/$PROJECT_ID/pypi"

gcloud run deploy "pypi" --quiet \
    --image "gcr.io/$PROJECT/pypi" \
    --port 80 \
    --platform "managed" \
    --allow-unauthenticated \
    --region europe-west1
```

Get the url of your service by running and selecting option 1 - Cloud Run (fully managed) 

```
gcloud run services list
```

Test your connection to the registry

```
REGISTRY_URL=https://<UNIQUE_SERVICE_IDENTIFIER>.a.run.app
pip search --index $REGISTRY_URL example
```

### Useful Resources
* [Python Packages Documentation](https://python-packaging.readthedocs.io/en/latest/minimal.html#)
* [Documentation on how to add external dependencies to Python Packaging](https://python-packaging.readthedocs.io/en/latest/dependencies.html)
