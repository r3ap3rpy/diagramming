from diagrams import Cluster, Diagram

from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3

with Diagram("Event Proc"):
	source = EKS("k8s source")
	with Cluster("Event Flows"):
		workers = [ECS("w1"),ECS("w2"),ECS("w3")]
	queue = SQS("event queue")
	with Cluster("Processing"):
		handlers = [Lambda("P1"),Lambda("P2"),Lambda("P3")]
	store = S3("events store")
	dw = Redshift("analytics")
	source >> workers >> queue >> handlers
	handlers >> store
	handlers >> dw
