import pandas as pd


class VertexMinifier:

    def __init__(self):
        pass


    def minify(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        minify an input dataframe
        """

        df_min = df.loc[
            (df["name"].str.lower().str.contains("vulpes")) |
            (df["name"].str.lower().str.contains("canis")) |
            (df["name"].str.lower().str.contains("felis")) |
            (df["name"].str.lower().str.contains("panthera")) |
            (df["name"].str.lower().str.contains("pantherinae")) |
            (df["name"].str.lower().str.contains("sciurus")) |
            (df["name"].str.lower().str.contains("sciurini")) |
            (df["name"].str.lower().str.contains("sciuridae")) |
            (df["name"].str.lower().str.contains("sciurinae")) |
            (df["name"].str.lower().str.contains("rodentia")) |
            (df["name"].str.lower().str.contains("canidae")) |
            (df["name"].str.lower().str.contains("felinae")) |
            (df["name"].str.lower().str.contains("felidae")) |
            (df["name"].str.lower().str.contains("feliformia")) |
            (df["name"].str.lower().str.contains("caniformia")) |
            (df["name"].str.lower().str.contains("carnivora")) |
            (df["name"].str.lower().str.contains("eutheria")) |
            (df["name"].str.lower().str.contains("theria")) |
            (df["name"].str.lower().str.contains("mammalia")) |
            (df["name"].str.lower().str.contains("chordata")) |
            (df["name"].str.lower().str.contains("tetrapoda")) |
            (df["name"].str.lower().str.contains("animalia")) |
            (df["name"].str.lower().str.contains("eukaryota")) |
            (df["name"].str.lower().str.contains("erithacus")) |
            (df["name"].str.lower().str.contains("muscicapidae")) |
            (df["name"].str.lower().str.contains("passeriformes")) |
            (df["name"].str.lower().str.contains("passeridae")) |
            (df["name"].str.lower().str.contains("passer")) |
            (df["name"].str.lower().str.contains("aves")) |
            (df["name"].str.lower().str.contains("turdidae")) |
            (df["name"].str.lower().str.contains("turdus")) |
            (df["name"].str.lower().str.contains("corvus")) |
            (df["name"].str.lower().str.contains("corvinae")) |
            (df["name"].str.lower().str.contains("corvidae")) |
            (df["name"].str.lower().str.contains("corvoidea")) |
            (df["name"].str.lower().str.contains("cervidae")) |
            (df["name"].str.lower().str.contains("cervus")) |
            (df["name"].str.lower().str.contains("capreolus")) |
            (df["name"].str.lower().str.contains("capreolinae"))
        ]

        return df_min
