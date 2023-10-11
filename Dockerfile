# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Set environment variables (replace 'password' with your actual password)
ENV POSTGRES_PASSWORD=password

# Install dependencies and build pgvector
RUN apt-get update && apt-get install -y sudo git postgresql-server-dev-16 make gcc locales \
    && git clone --branch v0.5.0 https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make \
    && make install \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Reconfigure locales
RUN echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && locale-gen

# Expose the PostgreSQL service port
EXPOSE 5432
