# Murder Mystery application
## Running with a venv

create a virtual environment, 

```
virtualenv ${venv_name}
# or
python -m virtualenv ${venv_name}
# then source it
source ${venv_name}/bin/activate
```

source it and then run the following:

```
pip install -r requirements.txt
```

Run the program with all users on the same network and have them connect to your IP at port 8000:

```
daphne mywebsite.asgi:application --bind  0.0.0.0
```

## Running with Docker/Podman

Build the image
```
podman build -t murdermystery ./murdermystery
```
Run the container
```
podman run -p 8000:8000 -d murdermystery
```

