# Catalogue Of Life

## Localhost Gremlin Server

```bash
docker run --rm -it -p 8182:8182 --name gremlin tinkerpop/gremlin-server
```

## Data Model

### taxon

- col_id: str (pk, unique)
- parent_id: str
- accepted_id: str
- taxonomic_status: str
- rank: str
- name: str
- authority: str
- language: str

### vernacular_name

1:m relation taxon:vernacular_name

- col_id str
- language: str
- name: str

### species_profile

1:1 relation taxon:species_profile (nullable)

- col_id: str
- is_extinct: bool
- is_marine: bool
- is_freshwater: bool
- is_terrestrial: bool

### distribution

1:m relation taxon:distribution (nullable)

- col_id: str
- occurence_status: str
- location_id: str
- locality: str

## Gremlin Model

total vertices: 5265100
total edges: 2630733

### Vertices

- ~id: col_id (str)
- parent_id: str
- accepted_id: str
- taxonomic_status: str
- rank: str
- name: str
- authority: str
- language: str
- is_extinct: bool
- is_marine: bool
- is_freshwater: bool
- is_terrestrial: bool

### Edges

- ~id: index
- ~from: col_id
- ~to: parent_id
- ~label: parent

[test-gremlin-loader](https://contextualise.dev/topics/view/15/gremlin)
