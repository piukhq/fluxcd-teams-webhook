FROM python:3.8-slim as base
WORKDIR /app
COPY poetry.lock /app
COPY pyproject.toml /app
RUN pip3.8 install poetry && \
    poetry export -f requirements.txt > requirements.txt

FROM python:3.8-slim as build
WORKDIR /app
COPY --from=base /app/requirements.txt /app/
RUN pip3.8 install -r requirements.txt
COPY fluxcd_teams_bot /app/fluxcd_teams_bot/

EXPOSE 8080


CMD ["python3", "-m", "fluxcd_teams_bot.server"]