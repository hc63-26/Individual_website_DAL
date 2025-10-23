FROM python:3.11-slim

# set a working directory
WORKDIR /app

# system deps for some packages (none strictly required here but kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# create a non-root user to run the app
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# default port used by Flask
EXPOSE 5000

# run with binding to 0.0.0.0 to be reachable from outside the container
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "app.py"]
