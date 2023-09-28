#!pip install pykeen
#!pip install git+https://github.com/pykeen/pykeen.git

import pandas as pd
import pykeen
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.hpo import hpo_pipeline
from optuna.samplers import GridSampler
from optuna.samplers import RandomSampler
from pykeen import predict
from pykeen.predict import predict_all
from pykeen.predict import predict_triples
from pykeen.datasets import get_dataset
import torch

import matplotlib.pyplot as plt


file_path = "/Users/cenxitoh/Desktop/Project/Ontology_Mapping/Mapping_Modified.txt"

tf = TriplesFactory.from_path(file_path)


result = pipeline(
        training=tf,
        testing=tf,
        dataset_kwargs={'create_inverse_triples': True},
        model = "DistMult",
        model_kwargs=dict(embedding_dim=128),
        training_kwargs=dict(num_epochs=300),
        random_seed=64)



result.plot_losses()
plt.show()



# get entity labels from training set
entity_labels = tf.entity_labeling.all_labels()
# convert entities to ids
entity_ids = torch.as_tensor(tf.entities_to_ids(entity_labels))
# retrieve the embeddings using entity ids
entity_embeddings = result.model.entity_representations[0](indices=entity_ids)
# create a dictionary of entity labels and embeddings
entity_embeddings_cpu = entity_embeddings.detach().cpu().numpy()
entity_embeddings_dict = dict(zip(entity_labels, entity_embeddings_cpu))




# get relation labels from training set
relation_labels = tf.relation_labeling.all_labels()
# convert relations to ids
relation_ids = torch.as_tensor(tf.relations_to_ids(relation_labels))
# retrieve the embeddings using relation ids
relation_embeddings = result.model.relation_representations[0](indices=relation_ids)
# create a dictionary of relation labels and embeddings
relation_embeddings_cpu = relation_embeddings.detach().cpu().numpy()
relation_embeddings_dict = dict(zip(relation_labels, relation_embeddings_cpu))




#Triple Scoring
pack = predict_triples(model=result.model, triples = tf)
df = pack.process(factory = result.training).df
df.to_csv('KnowledgeGraph_Embedding/DistMult_Triples.csv', index=False)


# Metric results
metric_results = result.metric_results.to_df()
metric_results.to_csv('KnowledgeGraph_Embedding/DistMult_Metrics.csv')