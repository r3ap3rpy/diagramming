from diagrams import Diagram
from diagrams.custom import Custom
from diagrams.aws.analytics import Athena
with Diagram("Custom Provider"):
  ds = Custom("Shotgun","./ds.jpeg")
  a = Athena("athena")
  ds >> a
