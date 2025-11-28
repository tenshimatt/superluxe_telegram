FROM python:3.7-slim

WORKDIR /botname

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /botname/
RUN pip install --no-cache-dir -r /botname/requirements.txt
COPY . /botname/

# Make sure the database directory exists
RUN mkdir -p /botname/data

CMD ["python3", "/botname/app.py"]