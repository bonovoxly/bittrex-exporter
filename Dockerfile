FROM python:3.6
RUN pip install prometheus_client requests
RUN mkdir -p /opt/bittrex-exporter
COPY ./Dockerfile /opt/bittrex-exporter/
COPY ./README.md /opt/bittrex-exporter/
COPY ./bittrex.py /opt/bittrex-exporter/
WORKDIR /opt/bittrex-exporter

ENTRYPOINT ["python3", "bittrex.py"]
