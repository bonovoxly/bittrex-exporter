from prometheus_client import start_http_server, Metric, REGISTRY
import argparse
import json
import logging
import requests
import sys
import time

# logging setup
log = logging.getLogger('bittrex-exporter')
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

class BittrexCollector():
  def __init__(self):
    self.getmarketsummaries = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'

  def collect(self):
    # query the api
    r = requests.get(self.getmarketsummaries)
    request_time = r.elapsed.total_seconds()
    log.info('elapsed time -' + str(request_time))
    response = json.loads(r.content.decode('UTF-8'))
    # setup the metric
    metric = Metric('bittrex_response_time', 'Total time for the bittrex API to respond.', 'summary')
    # add the response time as a metric
    metric.add_sample('bittrex_response_time', value=float(request_time), labels={'name': 'bittrex.com'})
    yield metric
    metric = Metric('bittrex', 'bittrex metric values', 'gauge')
    for each in response['result']:
      for that in ['High', 'Low', 'Volume', 'Last', 'BaseVolume', 'Bid', 'Ask', 'OpenBuyOrders', 'OpenSellOrders', 'PrevDay']:
        if each[that] is not None:
            metric.add_sample('bittrex', value=float(each[that]), labels={'MarketName': each['MarketName'], 'Type': that})
    yield metric

if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', nargs='?', const=9101, help='The TCP port to listen on.  Defaults to 9101.', default=9101)
    args = parser.parse_args()
    log.info(args.port)
  
    REGISTRY.register(BittrexCollector())
    start_http_server(int(args.port))
    while True:
      time.sleep(60)
  except KeyboardInterrupt:
    print(" Interrupted")
    exit(0)
