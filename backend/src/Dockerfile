FROM python:3.12

WORKDIR /src

# ✅ Install PostgreSQL client tools for pg_isready
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /src/entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]