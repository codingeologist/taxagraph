import os
import sys
import csv
import logging
import multiprocessing
from datetime import datetime
from gremlin_python.structure.graph import Graph
from gremlin_python.process.traversal import T
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


os.makedirs("logs", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/graph_load_{timestamp}.log"


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


def clear_graph():

    g, conn = get_traversal()

    try:
        g.V().drop().iterate()
        g.E().drop().iterate()
        logging.info(f"Cleared graph vertices and edges")
    except Exception as ex:
        logging.error(f"Error clearing graph vertices and edges: {ex}", exc_info=True)
    finally:
        conn.close()


def load_vertices(batch):

    g, conn = get_traversal()
    try:
        if model == "catalogue-of-life":
            for row in batch:
                g.addV(row["label"]) \
                    .property(T.id, row["id"]) \
                    .property("col_id", row["col_id"]) \
                    .property("col_parent", row["col_parent"]) \
                    .property("accepted_id", row["accepted_id"]) \
                    .property("taxonomic_status", row["taxonomic_status"]) \
                    .property("rank", row["rank"]) \
                    .property("name", row["name"]) \
                    .property("authority", row["authority"]) \
                    .property("is_extinct", row["is_extinct"]) \
                    .property("is_marine", row["is_marine"]) \
                    .property("is_freshwater", row["is_freshwater"]) \
                    .property("is_terrestrial", row["is_terrestrial"]) \
                    .iterate()
        elif model == "uksi":
            for row in batch:
                g.addV(row["label"]) \
                    .property(T.id, row["id"]) \
                    .property("uksi_tvk", row["uksi_tvk"]) \
                    .property("parent_id", row["parent_id"]) \
                    .property("recommended_uksi_tvk", row["recommended_uksi_tvk"]) \
                    .property("name", row["name"]) \
                    .property("authority", row["authority"]) \
                    .property("qualifier", row["qualifier"]) \
                    .property("language", row["language"]) \
                    .property("rank", row["rank"]) \
                    .property("recommended", row["recommended"]) \
                    .property("taxonomy", row["taxonomy"]) \
                    .iterate()
        logging.info(f"Processed batch of {len(batch)}, vertices")
    except Exception as ex:
        logging.error(f"Error processing vertex batch: {ex}", exc_info=True)
    finally:
        conn.close()


def load_edges(batch):

    g, conn = get_traversal()
    try:
        if model == "catalogue-of-life":
            for row in batch:
                # # parent relations
                g.V().has("col_id", row["from"]).as_("src") \
                    .V().has("col_id", row["to"]).as_("tgt") \
                    .addE(row["label"]).from_("src").to("tgt").iterate()
                # # sibling relations
                # g.V().has("col_id", row["from"]).as_("src") \
                #     .V().has("col_parent", row["to"]).as_("tgt") \
                #     .addE("sibling").from_("src").to("tgt").iterate()
        elif model == "uksi":
            for row in batch:
                g.V().has("uksi_tvk", row["from"]).as_("src") \
                    .V().has("uksi_tvk", row["to"]).as_("tgt") \
                    .addE(row["label"]).from_("src").to("tgt").iterate()
        logging.info(f"Processed batch of {len(batch)}, vertices")
    except Exception as ex:
        logging.error(f"Error processing vertex batch: {ex}", exc_info=True)
    finally:
        conn.close()


def read_csv_chunk(file_path: str, chunk_size=1000):

    with open(file=file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        batch = []
        for row in reader:
            batch.append(row)
            if len(batch) >= chunk_size:
                yield batch
                batch = []
        if batch:
            yield batch


def parallel_load(csv_file: str, num_processes: int, chunk_size: int, mode="vertices"):

    pool = multiprocessing.Pool(processes=num_processes)
    task_func = load_vertices if mode == "vertices" else load_edges

    logging.info(f"Starting parallel load with {num_processes} processess...")
    batch_count = 0

    try:
        batches = list(read_csv_chunk(file_path=csv_file, chunk_size=chunk_size))
        batch_count = len(batches)
        logging.info(f"Prepared {batch_count} batches from {csv_file}")
        pool.map(task_func, batches)
    except Exception as ex:
        logging.error(f"Error during parallel load: {ex}", exc_info=True)
    finally:
        pool.close()
        pool.join()
        logging.info(f"Completed processing {batch_count} batches")


def main(model: str):

    logging.info("Starting new GraphDB load...")
    clear_graph()
    parallel_load(csv_file=f"{model}/data/vertices_min.csv", num_processes=16, chunk_size=1000, mode="vertices")
    logging.info("Vertices loaded")
    parallel_load(csv_file=f"{model}/data/edges.csv", num_processes=16, chunk_size=1000, mode="edges")
    logging.info("Edges loaded")
    logging.info("Process completed!")


if __name__ == "__main__":

    model = input("taxononomy model:")
    if model == "catalogue-of-life" or model == "uksi":
        logging.info(f"{model} data")
        main(model=model)
