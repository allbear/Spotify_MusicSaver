FROM python:3.9
USER root

RUN apt update

RUN apt install libffi-dev

WORKDIR /code
ADD . .

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install mysql-connector-python
RUN python -m pip install spotipy
RUN python -m pip install python-dotenv
RUN python -m pip install requests
CMD ["python", "main.py"]