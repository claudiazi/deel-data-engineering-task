FROM python:3.11-slim

# Declare a build argument with a default value.
ARG DESKTOP_PATH=/Users/default/Desktop

# Set an environment variable from the build argument.
ENV DESKTOP_PATH=${DESKTOP_PATH}

COPY . .

RUN pip install --no-cache-dir --quiet --progress-bar off -r requirements.txt

CMD [ "python", "csv_report.py" ]
