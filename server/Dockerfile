FROM qfortier/poetry

WORKDIR /server

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .

EXPOSE 5000

CMD ["poetry", "run", "python", "app.py"]
