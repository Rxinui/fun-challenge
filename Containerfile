# wip
FROM python:3.12-alpine
WORKDIR /app
COPY .  ./
ENTRYPOINT [ "python" ]