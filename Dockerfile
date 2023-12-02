ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD python3 script.py
