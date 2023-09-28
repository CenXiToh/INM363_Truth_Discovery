## INM363 Individual Project - Truth Discovery

This repository is organized into several folders, each serving specific purposes within the project workflow. Due to the confidential nature of the data, not all documents are included in this repository.

The scraped data from HomeX, which was used to create the Universal Diagnostic Table (UDT), and the associated scripts are not included.


### Ontology Mapping:

The data folder contains the modified data in Universal Diagnostic Table (UDT) format that is currently being mapped. Here are the relevant files:

Refrigerator_Modified.csv: This file is used for Knowledge Graph Embedding and contains both reference and test data.

Refrigerator_Train.csv: This file is utilized for Sentence Embedding and contains reference data.

Refrigerator_Test.csv: This file is also used for Sentence Embedding and contains test data. 

(Reference data includes information from Repair Clinic and Fix, while test data is created for contradictory phrases).

Please note that the script used to create the ontology is not included in this repository, but the script responsible for mapping UDT to the ontology is provided.

### KG Embeddings:

Inside this folder, you'll discover scripts for various knowledge graph embedding methods, including TransR, DistMult, and ConvE. These scripts make use of the PyKEEN library. It's important to note that the data utilized by these scripts originates from the Ontology Mapping section and is not included here. Additionally, the results of embedding for each model, which encompass the triple scoring for all the triples, as well as the metric results, are not included.

### Sentence Embeddings:

In this folder, you'll find the script for sentence embedding. Just like the KG Embeddings section, the data used here is also the output from the Ontology Mapping section and is not included in this repository. However, we have included the "sentence_embeddings_results.csv" file, which contains the output and results of the sentence embeddings.
