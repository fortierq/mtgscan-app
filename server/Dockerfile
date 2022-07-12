FROM python:3.8

RUN useradd -ms /bin/bash user
USER user
ENV PATH /home/user/.local/bin:$PATH

WORKDIR /server

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]
