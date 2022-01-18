from diagrams import Cluster, Diagram

from diagrams.custom import Custom
from diagrams.aws.database import Aurora
from diagrams.k8s.compute import Pod

from urllib.request import urlretrieve

url = "https://jpadilla.github.io/rabbitmqapp/assets/img/icon.png"
icon = "rabbitmq.png"
urlretrieve(url, icon)

with Diagram("Broker"):
	with Cluster("Consumers"):
		consumers = [Pod("w1"), Pod("w2"), Pod("w3")]
	queue = Custom("Message queue", icon)
	queue >> consumers >> Aurora("Database")
