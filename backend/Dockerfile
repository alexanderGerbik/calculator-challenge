# syntax=docker/dockerfile:1.3
FROM python:3.12.2-slim AS base

FROM base AS requirements
RUN pip install --disable-pip-version-check poetry
WORKDIR /src
COPY pyproject.toml poetry.lock /src/
RUN poetry export -f requirements.txt --without-hashes -o /src/requirements.txt
RUN poetry export -f requirements.txt --dev --without-hashes -o /src/dev-requirements.txt

FROM base as main
WORKDIR /src
COPY --from=requirements /src/requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt
COPY . /src/
ENTRYPOINT ["/usr/local/bin/python3"]
CMD ["app.py"]
EXPOSE 8000


FROM main AS dev-image
COPY --from=requirements /src/dev-requirements.txt /dev-requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /dev-requirements.txt


FROM main AS final
