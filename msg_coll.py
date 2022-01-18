from diagrams import Diagram, Cluster

from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import BigTable
from diagrams.gcp.iot import IotCore 
from diagrams.gcp.storage import GCS

with Diagram("Message Collection"):
	pubsub = PubSub("pubsub")
	with Cluster("Source"):
		[IotCore("core1"),IotCore("core2"), IotCore("core3")] >> pubsub
	with Cluster("Targets"):
		with Cluster("Data Flow"):
			flow = Dataflow("flow")
		with Cluster("Data Lake"):
			flow >> [BigQuery("bq"), GCS("storage")]
		with Cluster("Event Driven"):
			with Cluster("Processing"):
				flow >> AppEngine("engine") >> BigTable("bt")
			with Cluster("Serverless"):
				flow >> Functions("func") >> AppEngine("appengine")
	pubsub >> flow
