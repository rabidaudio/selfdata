FROM python:3.10

ENV PYTHONUNBUFFERED 1
WORKDIR /project
ENV PATH="/project/.venv/bin:$PATH"
EXPOSE 3000

RUN apt-get update && \
  apt-get install -yy \
  curl jq nano postgresql-client iputils-ping

RUN mkdir .venv && \
  pip3 install --upgrade pip && \
  python3 -m venv .venv && \
  .venv/bin/pip3 install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY meltano.yml meltano.yml
COPY orchestrate/setup.py orchestrate/setup.py
RUN meltano install

COPY . .
# RUN meltano invoke dbt-athena deps
