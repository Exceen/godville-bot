FROM python:3.12.4-alpine@sha256:b7662fc33e07f05fb2f579c3634e1e4d2e30c02553397c6c24f775cb360dbc03 AS builder

# Prevent Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keep Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

# Enable custom virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# renovate: datasource=pypi depName=pip versioning=pep440
ARG PIP_VERSION="24.1.1"

# Set the working directory
WORKDIR /app

# Add requirements file
COPY requirements.txt .

# Install requirements
RUN python3 -m venv ${VIRTUAL_ENV} && \
    pip install --no-cache-dir --upgrade pip=="${PIP_VERSION}" && \
    pip install --no-cache-dir -r requirements.txt



FROM python:3.12.4-alpine@sha256:b7662fc33e07f05fb2f579c3634e1e4d2e30c02553397c6c24f775cb360dbc03

# renovate: datasource=pypi depName=pip versioning=pep440
ARG PIP_VERSION="24.1.1"

# renovate: datasource=repology depName=alpine_3_20/firefox versioning=loose
# ARG FIREFOX_VERSION="126.0.1-r0"
ARG FIREFOX_VERSION="132.0.2-r0"

# renovate: datasource=repology depName=alpine_3_20/font-noto versioning=loose
ARG FONT_MOTO_VERSION="23.7.1-r0"

# renovate: datasource=repology depName=alpine_edge/geckodriver versioning=loose
ARG GECKODRIVER_VERSION="0.34.0-r0"

# renovate: datasource=repology depName=alpine_3_20/openssl versioning=loose
ARG OPENSSL_VERSION="3.3.1-r1"

# renovate: datasource=repology depName=alpine_3_20/expat versioning=loose
ARG EXPAT_VERSION="2.6.2-r0"

RUN apk add --no-cache firefox="${FIREFOX_VERSION}" font-noto=="${FONT_MOTO_VERSION}" && \
    apk add --no-cache --repository=https://dl-cdn.alpinelinux.org/alpine/edge/community geckodriver="${GECKODRIVER_VERSION}" && \
    ln -s /usr/bin/geckodriver /usr/local/bin/geckodriver && \
    rm -rf /var/cache/apk/* /tmp/*

# Fix vulnerabilities reported by Trivy
RUN apk add --no-cache libcrypto3="${OPENSSL_VERSION}" libssl3="${OPENSSL_VERSION}" libexpat="${EXPAT_VERSION}" && \
    /usr/local/bin/pip install --upgrade pip=="${PIP_VERSION}"

# Enable custom virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy dependencies from previous stage
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

# Set the working directory
WORKDIR /app

# Copy and set the entrypoint bash script
COPY godville.py .
COPY main.py .
COPY .env .
# COPY . .
ENTRYPOINT ["python", "./main.py"]
