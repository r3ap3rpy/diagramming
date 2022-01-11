from diagrams import Diagram

from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Grouped Workers", show = True, direction="TB"):
    ELB("lb") >> [EC2("worker1"),EC2("worker2"),EC2("worker3")] >> RDS("events")
