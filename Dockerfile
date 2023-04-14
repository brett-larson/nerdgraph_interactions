FROM python:3.11

WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the New Relic configuration file environment variable
ENV NEW_RELIC_CONFIG_FILE=newrelic.ini

# Copy the New Relic configuration file into the container
COPY newrelic.ini .

# Copy the rest of the application code
COPY . .

# Copy the .env file into the container
COPY .env .

# Set the ENTRYPOINT for New Relic monitoring
ENTRYPOINT ["newrelic-admin", "run-program"]

# Set the CMD to run your Python script
CMD ["python", "main.py"]
