FROM python:3-alpine

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
LABEL name="ghcr.io/cdot65/pan-os-docker"
LABEL maintainer="cremsburg.dev@gmail.com"
LABEL description="Alpine based Python container for Palo Alto Networks SDK."
LABEL license="Apache 2.0"
LABEL url="https://github.com/cdot65/pangpt"
LABEL build-date="20230306"

# ---------------------------------------------------------------------------
# Install dependencies and Python packages
# ---------------------------------------------------------------------------
ADD requirements.txt /var/tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /var/tmp/requirements.txt

# ---------------------------------------------------------------------------
# Declare environmentals
# ---------------------------------------------------------------------------
ARG SLACK_BOT_TOKEN
ARG SLACK_APP_TOKEN
ARG SLACK_CHANNEL
ARG OPENAI_TOKEN

ENV SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN
ENV SLACK_APP_TOKEN=$SLACK_APP_TOKEN
ENV SLACK_CHANNEL=$SLACK_CHANNEL
ENV OPENAI_TOKEN=$OPENAI_TOKEN
