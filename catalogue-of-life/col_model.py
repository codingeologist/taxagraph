import os
import pandas as pd

dist = pd.read_csv("raw/Distribution.tsv", sep="\t")
dist = dist.iloc[:, [0, 1, 2, 3]]
dist.columns = ["col_id", "occurrence_status", "location_id", "locality"]

profile = pd.read_csv("raw/SpeciesProfile.tsv", sep="\t")
profile = profile.iloc[:, [0, 1, 2, 3, 4]]
profile.columns = ["col_id", "is_extinct", "is_marine", "is_freshwater", "is_terrestrial"]

names = pd.read_csv("raw/VernacularName.tsv", sep="\t")
names = names.iloc[:, [0, 1, 2]]
names.columns = ["col_id", "language", "name"]

taxon = pd.read_csv("raw/Taxon.tsv", sep="\t", low_memory=False)
taxon = taxon.iloc[:, [0, 1, 2, 6, 7, 8, 9]]
taxon.columns = ["col_id", "parent_id", "accepted_id", "taxonomic_status", "rank", "name", "authority"]

def split_name(row):
    return row["name"].split(" {}".format(row["authority"]))[0]
taxon["name"] = taxon.apply(split_name, axis=1)

if not os.path.exists(f"data"):
    os.makedirs(f"data")
dist.to_csv("data/distribution.csv", index=False)
profile.to_csv("data/species_profile.csv", index=False)
names.to_csv("data/vernacular_name.csv", index=False)
taxon.to_csv("data/taxon.csv", index=False)
