from diagrams import Cluster, Diagram

from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram("Advanced on prem"):
	ingress = Nginx("ingress")
	metrics = Prometheus("metrics")
	metrics << Grafana("monitoring")

	with Cluster("Service Cluster"):
		grpsvc = [Server("s1"),Server("s2"),Server("s3")]
	
	with Cluster("Session HA"):
		main = Redis("session")
		main - Redis("replica") << metrics
		grpsvc >> main
	
	with Cluster("Database HA"):
		main = PostgreSQL("users")
		main - PostgreSQL("replica") << metrics
		grpsvc >> main

	aggregator = Fluentd("logging")
	aggregator >> Kafka("stream") >> Spark("analytics")
	ingress >> grpsvc >> aggregator
