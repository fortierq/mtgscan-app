# https://www.docker.com/blog/containerized-python-development-part-1/

FROM python:3.8
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "app.py"]
