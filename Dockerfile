FROM python:3.12-slim-bookworm

RUN apt-get update # && apt-get install -y --no-install-recommends \

RUN pip install .

CMD ["cf-dyndns"]
