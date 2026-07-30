import os
import sys
import logging
import pandas as pd
from datetime import datetime
from minifier import VertexMinifier


os.makedirs("logs", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/graph_model_{timestamp}.log"
mini = VertexMinifier()


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s/%(processName)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)


def uksi(model: str):

    vertices = pd.read_csv(f"{model}/data/taxon.csv", low_memory=False)
    vertices.insert(loc=0, column="id", value=vertices.index)
    vertices.loc[:, "label"] = "taxon"
    vertices = vertices.rename(columns={
        "recommended_scientific_name": "name"
    })
    vertices.to_csv(f"{model}/data/vertices.csv", index=False)
    logging.info(f"total vertices: {len(vertices)}")

    logging.info(f"minifying vertices...")
    vertices_min = mini.minify(df=vertices)

    vertices_min.to_csv(f"{model}/data/vertices_min.csv", index=False)
    logging.info(f"total vertices (minified): {len(vertices_min)}")

    with_parent = vertices_min.loc[vertices_min["parent_id"].isin(vertices_min["uksi_tvk"])]
    with_parent.loc[:, "label"] = "parent"
    with_parent = with_parent.rename(columns={
        "uksi_tvk": "from",
        "parent_id": "to"
    })
    with_parent = with_parent[["from", "to", "label"]].reset_index(drop=True)
    with_parent.insert(loc=0, column="id", value=with_parent.index)
    with_parent.to_csv(f"{model}/data/edges.csv", index=False)

    logging.info(f"total edges: {len(with_parent)}")


def catalogue_of_life(model: str):

    taxon = pd.read_csv(f"{model}/data/taxon.csv", low_memory=False)
    species_profile = pd.read_csv(f"{model}/data/species_profile.csv", low_memory=False)

    vertices = pd.merge(left=taxon, right=species_profile, how="left", on="col_id")
    vertices.insert(loc=0, column="id", value=vertices.index)
    vertices = vertices.rename(columns={
        "parent_id": "col_parent"
    })
    vertices.loc[:, "label"] = "taxon"
    vertices.to_csv(f"{model}/data/vertices.csv", index=False)
    logging.info(f"total vertices: {len(vertices)}")

    logging.info(f"minifying vertices...")
    vertices_min = mini.minify(df=vertices)

    vertices_min.to_csv(f"{model}/data/vertices_min.csv", index=False)
    logging.info(f"total vertices (minified): {len(vertices_min)}")

    # with_parent = vertices.loc[vertices["parent_id"].notnull()].reset_index()
    with_parent = vertices_min.loc[vertices_min["col_parent"].isin(vertices_min["col_id"])]
    with_parent.loc[:, "label"] = "parent"
    with_parent = with_parent.rename(columns={
        "col_id": "from",
        "col_parent": "to"
    })
    with_parent = with_parent[["from", "to", "label"]].reset_index(drop=True)
    with_parent.insert(loc=0, column="id", value=with_parent.index)
    with_parent.to_csv(f"{model}/data/edges.csv", index=False)

    logging.info(f"total edges: {len(with_parent)}")


if __name__ == "__main__":

    model = input("taxonomy model:")
    logging.info(f"{model} data")
    if model == "catalogue-of-life":
        catalogue_of_life(model=model)
    elif model == "uksi":
        uksi(model=model)
