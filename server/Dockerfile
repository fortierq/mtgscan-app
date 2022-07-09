FROM python:3.9

RUN python3 -m pip install --upgrade pip &&\   
    curl -sSL https://install.python-poetry.org | python3 -
    
WORKDIR /app

COPY pyproject.toml ./

ENV PATH="/root/.local/bin:${PATH}"

RUN poetry install

EXPOSE 5000

CMD ["poetry", "run", "python", "/app/app.py"]