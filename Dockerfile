FROM python:3.12-slim

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# gosu lets the entrypoint start as root (to fix ownership of the
# /media volume, which Docker creates as root:root) and then drop
# privileges to appuser before running gunicorn.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gosu \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

RUN chmod +x entrypoint.sh \
    && mkdir -p /app/staticfiles \
    && adduser --disabled-password --no-create-home --gecos "" appuser \
    && chown -R appuser:appuser /app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health/')" || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
