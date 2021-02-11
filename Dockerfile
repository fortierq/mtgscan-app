# https://www.docker.com/blog/containerized-python-development-part-1/

FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src src

CMD ["python", "src/server.py"]
