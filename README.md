create a virtual environment, 

virtualenv <whatever_name>  or python virtualenv <whatever_name>

source it and then run the following:

pip install daphne

pip install django

pip install  channels



Run the program with all users on the same network and have them connect to your IP at port 8000:

daphne mywebsite.asgi:application --bind  0.0.0.0
