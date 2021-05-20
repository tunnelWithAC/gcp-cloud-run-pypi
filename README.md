## Google Cloud Run PyPi registry

This repo contains code to build and deploy a PyPi registry to Google Cloud Run.

This project is an early stage proof of concept for how a private registry can be easily deployed and updated using Github Actions.

### How to build a package
Based on instructions from (here)[https://docs.gitlab.com/ee/user/packages/pypi_repository/#install-pip-and-twine]
See `packages/my_example_package` for an example of how to write `__init__.py` and `setup.py`

```
mkdir packages/my_new_package
cd packages/my_new_package
touch __init__.py setup.py <your_file_name>.py
# add your code  to <your_file_name>.py
# import your modules in __init__.py
# fill in your setup.py
python3 setup.py sdist bdist_wheel
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
* (Documentation on how to add external dependencies to Python Packaging)[https://python-packaging.readthedocs.io/en/latest/dependencies.html]