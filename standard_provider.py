from diagrams import Diagram
from diagrams.aws.analytics import Athena, Cloudsearch
from diagrams.gcp.analytics import Dataproc
with Diagram("Standard Provider"):
  a = Athena("Athena")
  c = Cloudsearch("Cloudsearch")
  d = Dataproc
  a >> c >> d
