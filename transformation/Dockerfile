FROM python:3.11-slim


RUN \
    # Install pre-requisites.
    apt-get update -yq && \
    apt-get install -yq --no-install-recommends \
        git bash && \
    # Clean-up system.
    apt-get clean -yq && \
    apt-get autoremove -yq && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*

WORKDIR /usr/local/src

COPY . .

RUN pip install --no-cache-dir --quiet --progress-bar off -r requirements.txt

ENV PYTHONPATH=/usr/local/src
ENV PYTHONUNBUFFERED=1

CMD ["bash", "run_dbt.sh"]
