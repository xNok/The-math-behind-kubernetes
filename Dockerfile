FROM python:3.12.8-slim-bookworm
LABEL authors="xnok"

ADD ./requirements.txt /app

RUN python3 -m pip install -r /app/requirements.txt

ADD ./models_or-tools /app/models_or-tools

RUN python3 -m pip install -e /app/models_or-tools

ENV PYTHONPATH="${PYTHONPATH}:/app/models_or-tools"

ENTRYPOINT ["python3", "/app/models_or-tools/problems/gcp_app_10_node_9.py"]
