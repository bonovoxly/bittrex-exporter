# prometheus-compose

This docker-compose file initializes a Prometheus and Grafana stack, including the bittrex exporter. It uses localhost ports 3000 and 9090.

To use:

- Start the docker-compose stack:

```
docker-compose up
```

- Go to <http://localhost:3000>.  Log in as `admin/admin`. 
- The Prometheus interface can be accessed at <http://localhost:9090>
