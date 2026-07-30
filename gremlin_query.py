import os
import sys
import json
import logging
from datetime import datetime
from gremlin_python.structure.graph import Graph
from gremlin_python.process.traversal import T
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


os.makedirs("logs", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/graph_query_{timestamp}.log"


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s/%(processName)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)


def get_traversal():

    conn = DriverRemoteConnection("ws://localhost:8182/gremlin", "g")
    graph = Graph()
    g = graph.traversal().withRemote(conn)

    return g, conn


def normalise_vertex(vertex: dict):

    normaised = {}
    for key, value in vertex.items():
        if key == T.id:
            key = str("id")
        elif key == T.label:
            key = str("label")
        else:
            key = str(key)
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        normaised[key] = value

    return normaised


def ancestor_traversal(g: Graph, name: str):

    query_data = g.V().has("name", name) \
        .union(
            __.identity(),
            __.repeat(__.out("parent")).emit()
        ) \
        .valueMap("name", "rank")
    
    return [normalise_vertex(vertex=vertex) for vertex in query_data]


def taxon_hierarchy(taxa: list, search_query: str):

    hierarchy = {
        "search_query": search_query,
        "match_status": "Taxon Hierarchy"
    }

    for taxon in taxa:
        rank = taxon.get("rank")
        name = taxon.get("name")
        
        if rank and name:
            hierarchy[rank] = name
    
    return hierarchy


if __name__ == "__main__":

    lookup = input("search for taxon name:")

    logging.info("Connecting to GraphDB...")
    g, conn = get_traversal()
    logging.info(f"Querying DB for taxon: {lookup}...")
    data = ancestor_traversal(g=g, name=lookup)
    logging.info("processing result...")
    result = taxon_hierarchy(taxa=data, search_query=lookup)

    os.makedirs("query-data", exist_ok=True)
    with open("query-data/query_response.json", "w") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    logging.info("Process completed!")
