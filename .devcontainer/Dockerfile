FROM python:3.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade colorlog black pylint

WORKDIR /workspace

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash
