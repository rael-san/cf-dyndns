FROM python:3.12-slim-bookworm

RUN apt-get update
#RUN apt-get update && apt-get install -y --no-install-recommends \

COPY . /cf-dyndns
WORKDIR /cf-dyndns
RUN pip install .

CMD ["cf-dyndns"]
