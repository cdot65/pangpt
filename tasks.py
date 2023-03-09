"""Tasks to execute with Invoke."""

# ---------------------------------------------------------------------------
# Python3.11 hack for invoke
# ---------------------------------------------------------------------------
import inspect

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

import os
from invoke import task

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_IMG = "ghcr.io/cdot65/pangpt"

ARM_TAG = "arm"
VERSION = "0.1.0"


# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# DOCKER CONTAINER BUILDS
# ---------------------------------------------------------------------------
@task(optional=["arm"])
def build(context, arm=None):
    """Build our Docker images."""
    if arm:
        context.run(
            f"docker build -t {DOCKER_IMG}:{ARM_TAG} --build-arg OPENAI_TOKEN --build-arg SLACK_APP_TOKEN --build-arg SLACK_BOT_TOKEN --build-arg SLACK_CHANNEL docker/arm",
        )
    else:
        context.run(
            f"docker build -t {DOCKER_IMG}:{VERSION} docker/intel",
        )


# ---------------------------------------------------------------------------
# SHELL ACCESS
# ---------------------------------------------------------------------------
@task(optional=["arm"])
def shell(context, arm=None):
    """Get shell access to the container."""
    if arm:
        context.run(
            f'docker run -it --rm \
                --mount type=bind,source="$(pwd)"/python,target=/home/python \
                -w /home/python/ \
                {DOCKER_IMG}:{ARM_TAG} /bin/sh',
            pty=True,
        )
    else:
        context.run(
            f'docker run -it --rm \
                --mount type=bind,source="$(pwd)"/terraform,target=/home/terraform \
                -w /home/terraform/ \
                {DOCKER_IMG}:{VERSION} /bin/sh',
            pty=True,
        )


# ---------------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------------
@task(optional=["arm"])
def local(context, arm=None):
    """Get access to the ipython REPL within our container."""
    if arm:
        context.run(
            f'docker run -it --rm \
                -v "$(pwd)"/app:/code/app \
                -p 8080:80 \
                -w /code \
                {DOCKER_IMG}:{ARM_TAG} uvicorn app.main:app --host 0.0.0.0 --port 80',
            pty=True,
        )
    else:
        context.run(
            f'docker run -it --rm \
                -v "$(pwd)"/app:/code/app \
                -p 8080:80 \
                -w /code \
                {DOCKER_IMG}:{VERSION} uvicorn app.main:app --host 0.0.0.0 --port 80',
            pty=True,
        )
