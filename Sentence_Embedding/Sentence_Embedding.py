import pandas as pd
from sentence_transformers import SentencesDataset, SentenceTransformer, InputExample, losses, util, evaluation
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


file_path = "/Users/cenxitoh/Desktop/Project_Python/Ontology_Mapping/Mapping_Train.csv"
file_path2 = "/Users/cenxitoh/Desktop/Project_Python/Ontology_Mapping/Mapping_Test.csv"


df = pd.read_csv(file_path)
df2 = pd.read_csv(file_path2)


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')



def analyze_similarity(df1, df2, predicates_to_include):
    df1["object"] = df1["object"].str.replace('_', " ")
    df2["object"] = df2["object"].str.replace('_', " ")

    # Filter the dataframes based on the specified predicates
    filtered_df1 = df1[df1["predicate"].isin(predicates_to_include)]
    filtered_df2 = df2[df2["predicate"].isin(predicates_to_include)]

    # Extract sentences from the dataframes
    sentences1 = filtered_df1['object'].tolist()
    sentences2 = filtered_df2['object'].tolist()

    # Initialize the sentence transformer model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Embed Repair Clinic phrases
    corpus1_embeddings = model.encode(sentences1, convert_to_tensor=True)

    result_data = []

    for sentence2 in sentences2:
        # Embed ChatGPT phrases
        sentence_embeddings = model.encode(sentence2, convert_to_tensor=True)

        cos_scores = util.pytorch_cos_sim(sentence_embeddings, corpus1_embeddings)[0]

        # Get the indices of the top-3 highest scores
        top_result_indices = np.argpartition(-cos_scores, range(5))[0:5]

        # Retrieve the top-3 highest scores and corresponding sentences
        result_data.append(f"Sentence: {sentence2}")
        result_data.append(f"Top 5 most similar sentences:")

        for idx, top_result_idx in enumerate(top_result_indices):
            highest_score = cos_scores[top_result_idx]
            reference_phrase = sentences1[top_result_idx]
            result_data.append(f"{reference_phrase} (Score: {highest_score:.4f})")
        result_data.append("\n")

    return result_data

def analyze_predicates(df1, df2, predicates):
    final_result_data = []

    for predicate in predicates:
        result_data = analyze_similarity(df1, df2, [predicate, "refrigerator/broken_compressor_pump"])
        final_result_data.extend(result_data)

    return final_result_data

df1 = df  # Assuming df and df2 are defined elsewhere in your code
df2 = df2
predicates = ["hasSymptom", "hasInvestigation", "hasInvestigationEquipment", "hasResolution", "hasResolutionEquipment", "hasResolutionMannerAttribute"]

result_data = analyze_predicates(df1, df2, predicates)

# Print the result data
#for item in result_data:
#    print(item)



result_data = pd.DataFrame(result_data)
result_data.to_csv("Sentence_Embedding/sentence_embeddings_results.csv", index = False)