import os
import pandas as pd

vert = pd.read_csv("raw/nodes_uksi.csv")
vert.drop(["recommended_rank", "taxonomy"], inplace=True, axis=1)
vert.rename(columns={"recommended_uksi_tvk": "uksi_tvk"}, inplace=True)

syns = pd.read_csv("raw/taxon_name_junior_synonym_uksi.csv")
syns_cols = list(syns)
syns_cols.insert(0, syns_cols.pop(syns_cols.index("uksi_tvk")))
syns_cols.insert(8, syns_cols.pop(syns_cols.index("taxonomy")))
syns = syns[syns_cols]

reco = pd.read_csv("raw/taxon_name_rec_sci_name_uksi.csv")
reco_cols = list(reco)
reco_cols.insert(0, reco_cols.pop(reco_cols.index("uksi_tvk")))
reco_cols.insert(8, reco_cols.pop(reco_cols.index("taxonomy")))
reco = reco[reco_cols]

# ignore synonyms for now as a left join on vertices and recommended attrs
# will result in some attrs being dropped if  the tvk is not in the vert df
vert_attrs = pd.merge(left=vert, right=reco, how="left", on="uksi_tvk")

if not os.path.exists(f"data"):
    os.makedirs(f"data")

vert_attrs.to_csv("data/taxon.csv", index=False)
