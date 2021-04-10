

Create compute engine instance

`gcloud compute instances create pypi-registry-example --zone=europe-west2-c --machine-type=e2-micro`

SSH into CE instance

`gcloud beta compute ssh --zone "europe-west2-c" "pypi-registry-example"  --project "conall-sandbox"`


Inside your CE

```
sudo apt-get update
sudo apt-get install python3-pip
pip3 install pypiserver

mkdir ~/packages
cd ~/packages/
mkdir conall-example && touch conall-example/__init__.py conall-example/hello_world.py

export PATH=$PATH:~/.local/bin
pypi-server -p 8080 ~/packages
```



pip search --index http://localhost:80 conall
pip install --extra-index http://localhost:80 conall-example


https://docs.gitlab.com/ee/user/packages/pypi_repository/#install-pip-and-twine

python3 setup.py sdist bdist_wheel


`docker build -t pypi . && docker run -80:80  --name pypi --rm -it pypi`