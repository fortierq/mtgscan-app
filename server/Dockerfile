FROM qfortier/poetry

EXPOSE 5000

WORKDIR /server
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "app.py"]
