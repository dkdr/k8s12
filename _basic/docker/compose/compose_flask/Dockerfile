FROM python:2.7
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY . /code/
WORKDIR /code
CMD python app.py