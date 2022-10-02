FROM python:3.10

WORKDIR /project
ENV PYTHONUNBUFFERED 1
ENV PATH="/project/.venv/bin:$PATH"
ENV FLASK_ENV=production \
    MELTANO_UI_FORWARDED_ALLOW_IPS="*" \
    MELTANO_UI_READONLY=true \
    MELTANO_UI_SESSION_COOKIE_SECURE=true \
    MELTANO_UI_SERVER_NAME=rabidaudio-selfdata.herokuapp.com
CMD meltano ui --bind-port $PORT

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
RUN meltano install

COPY . .
# RUN meltano invoke dbt-athena deps

# Heroku runs as non-root user, which complicates image building
RUN useradd -m selfdata
RUN chown -R selfdata /project
USER selfdata
