## Welcome

This repository holds source materials for my [diagrams]() video series..

You can find the official documentation [here](https://diagrams.mingrammer.com/docs/getting-started/installation).

In order to get started you need to install the prerequisites.

``` bash
git clone https://github.com/r3ap3rpy/diagramming.git
cd diagramming
virtualenv d
.\d\scripts\activate
pip install diagrams
```

You also need to install [Graphviz](https://graphviz.gitlab.io/download) as it is one of the dependencies.


#### Core concepts

###### Diagrams

They represent a global context and can be created with the **Diagram** class. The first parameter will become the filename unless the argument is specified.

``` python
from diagrams import Diagram
from diagrams.aws.compute import EC2

with Diagram("Simple Demo"):
    EC2("web")
```

You have the option to specify the **outputformat** argument which is by default **png**. With the **filename** you can customize the filename. Diagrams can be embedded into jupyter notebooks aswell.

You can pass attributes as a dictionary aswell.

``` python
from diagrams import Diagram
from diagrams.aws.compute import EC2

graph_attr = {"fontsize" : "39","bgcolor" : "transparent"}

with Diagram("Simple Diagram", graph_attr=graph_attr):
    EC2("Custom Attribute")
```

For further information on attributes you can visit the [graphwiz](https://www.graphviz.org/doc/info/attrs.html) site.


###### Node and Dataflow

Node is an abstract concept that represents a single object.

``` python
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ELB, Route53, VPC
```

The flow can be as follows.

**<<** connects nodes from left to right.
**>>** connects nodes from right to left.
**-** unidirection.

The direction of the flow can be changed with the **direction=** argument of the **Diagram** class the default is **LR**.

``` python
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Workers", show=False, direction="TB"):
    lb = ELB("lb")
    db = RDS("events")
    lb >> EC2("worker") >> db
```

You can group data flow if you put nodes inside a list.

``` python
ELB("lb") >> [EC2("worker1"),EC2("worker2"),EC2("worker3"),EC2("worker4"),EC2("worker5")] >> RDS("events")
```

###### Clusters

Clustering allows you to uut nodes into isolated groups, you need to import it from the base **diagrams** module.

You can connect nodes in a cluster to other nodes outside a cluster.

``` python
from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import Route53

with Diagram("Simple Web Service with DB Cluster", show=False):
    dns = Route53("dns")
    web = ECS("service")

    with Cluster("DB Cluster"):
        db_main = RDS("main")
        db_main - [RDS("replica1"),
                     RDS("replica2")]

    dns >> web >> db_main
```

You have the option to nest clusters aswell.

``` python
from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3

with Diagram("Event Processing", show=False):
    source = EKS("k8s source")

    with Cluster("Event Flows"):
        with Cluster("Event Workers"):
            workers = [ECS("worker1"),
                       ECS("worker2"),
                       ECS("worker3")]

        queue = SQS("event queue")

        with Cluster("Processing"):
            handlers = [Lambda("proc1"),
                        Lambda("proc2"),
                        Lambda("proc3")]

    store = S3("events store")
    dw = Redshift("analytics")

    source >> workers >> queue >> handlers
    handlers >> store
    handlers >> dw
```

###### Edges

An edge is representing an edge between nodes, it has three attributes **label**, **color** and **style**.


``` python
from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram(name="Advanced Web Service with On-Premise (colored)", show=False):
    ingress = Nginx("ingress")

    metrics = Prometheus("metric")
    metrics << Edge(color="firebrick", style="dashed") << Grafana("monitoring")

    with Cluster("Service Cluster"):
        grpcsvc = [
            Server("grpc1"),
            Server("grpc2"),
            Server("grpc3")]

    with Cluster("Sessions HA"):
        main = Redis("session")
        main \
            - Edge(color="brown", style="dashed") \
            - Redis("replica") \
            << Edge(label="collect") \
            << metrics
        grpcsvc >> Edge(color="brown") >> main

    with Cluster("Database HA"):
        main = PostgreSQL("users")
        main \
            - Edge(color="brown", style="dotted") \
            - PostgreSQL("replica") \
            << Edge(label="collect") \
            << metrics
        grpcsvc >> Edge(color="black") >> main

    aggregator = Fluentd("logging")
    aggregator \
        >> Edge(label="parse") \
        >> Kafka("stream") \
        >> Edge(color="black", style="bold") \
        >> Spark("analytics")

    ingress \
        >> Edge(color="darkgreen") \
        << grpcsvc \
        >> Edge(color="darkorange") \
        >> aggregator

```