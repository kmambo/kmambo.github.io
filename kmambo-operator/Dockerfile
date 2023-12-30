ARG FROM=python:3.12

FROM ${FROM} as base

# RUN addgroup -S kmambogroup
# RUN adduser -S kmambouser -G kmambogroup
RUN useradd -m kmambouser
WORKDIR /app

COPY src/kmambo /app/kmambo
COPY requirements.txt /app/requirements.txt
RUN python3.12 -m pip install --user -U setuptools pip
USER kmambouser
RUN python -m pip install -r /app/requirements.txt
ENV PYTHONPATH="/app:$PYTHONPATH"
