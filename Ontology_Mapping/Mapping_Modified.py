from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD
import pandas as pd
import csv
from pprint import pprint
import kglab
import copy
import owlrl


# Create an RDF graph
g1 = Graph()

# Load data from a Turtle file
turtle_file = "Ontology_Mapping/CUNO_script.ttl"
g1.parse(turtle_file, format="turtle")


homex = Namespace("http://example.org/homex#")
g1.bind("homex",homex)

df = pd.read_csv('/Users/cenxitoh/Desktop/Project_Python/Ontology_Mapping/Data/Refrigerator_Test.csv')


def is_empty_blank_node(graph, blank_node):
    # Iterate through triples with the given blank node as subject
    for triple in graph.triples((blank_node, None, None)):
        return False  # The blank node has outgoing triples
    for triple in graph.triples((None, None, blank_node)):
        return False  # The blank node has incoming triples
    return True


def construct_uri_component(label, value):
    if pd.isna(value):
        return ""
    return "/" + label + "-" + str(value).lower().replace(", ",",").replace("; ",",").replace(" ","_")


for quantity, artefact, brand, model_number, problem, symptom, investigation, investigation_equipment, resolution, resolution_manner, resolution_equipment in zip(df['Quantity'],df['Artefact'],df['Brand'],df['Model Number'],df['Artefact Problem'],df['Problem Symptoms'],df['Problem Investigation'],df['Artefacts Needed for Problem Investigation'],df['Problem Resolution'],df['Way of Carrying Out the Problem Resolution'],df['Artefacts Needed for Problem Resolution']):
    if not pd.isna(artefact):
        artefact_uri = homex + artefact.lower().replace(" ","_") + "/"

        if not pd.isna(brand) and brand != "N/A":
            artefact_uri += brand + "/"
        else:
            pass

        if not pd.isna(model_number) and model_number != "N/A":
            artefact_uri += str(model_number) + "/"
        else:
            pass

        if not pd.isna(problem) and problem != "N/A":
            artefact_uri += problem.lower().replace(" ", "_")
        else:
            pass

    else:
        pass

    if not pd.isna(problem):

        problem_uri = homex + problem.lower().replace(" ","_")    
        g1.add((URIRef(problem_uri), RDFS.subClassOf, homex.Issue))

    else:
        pass

    #Brand
    if(not pd.isna(brand)):
        brand_uri = homex + str(brand)
        g1.add((URIRef(brand_uri), RDF.type, homex.Brand))
    else:
        pass
        
    #ModelNumber
    if(not pd.isna(model_number)):
        model_number_uri = homex + str(model_number)
        g1.add((URIRef(model_number_uri), RDF.type, homex.ModelNumber))
    else:
        pass

    #Symptom    
    if(not pd.isna(symptom)) and symptom != "N/A":
        symptom_uri = homex + str(symptom).lower().replace(" ","_")
        g1.add((URIRef(symptom_uri), RDFS.subClassOf, homex.Issue))
    else:
        symptom_uri = None

    #Investigation 
    if(not pd.isna(investigation)) and investigation != "N/A":  
        investigation_uri = homex + str(investigation).lower().replace(" ","_")
        g1.add((URIRef(investigation_uri), RDF.type, homex.Investigation))
    else:
        investigation_uri = None
    
    #Investigation Equipment
    if(not pd.isna(investigation_equipment)) and investigation_equipment != "N/A":
        investigation_equipment_uri = homex + str(investigation_equipment).lower().replace(" ","_")
        g1.add((URIRef(investigation_equipment_uri), RDF.type, homex.Sort))
    else:
        investigation_equipment_uri = None

    #Resolution    
    if(not pd.isna(resolution)) and resolution != "N/A":
        resolution_uri = homex + str(resolution).lower().replace(" ","_")
        g1.add((URIRef(resolution_uri), RDF.type, homex.Resolution))
    else:
        resolution_uri = None

    #Resolution Manner   
    if(not pd.isna(resolution_manner)) and resolution_manner != "N/A": 
        resolution_manner_uri = homex + str(resolution_manner).lower().replace(" ","_")
        g1.add((URIRef(resolution_manner_uri), RDF.type, homex.MannerAttribute))
    else:
        resolution_manner_uri = None

    if (not pd.isna(resolution_equipment)) and resolution_equipment != "N/A":
        resolution_equipment_uri = homex + str(resolution_equipment).lower().replace(" ","_")
        g1.add((URIRef(resolution_equipment_uri), RDF.type, homex.Sort))
    else:
        resolution_equipment_uri = None



    #Create restrictions for each attribute

    restriction_brand = BNode()
    if(not pd.isna(brand)):
        g1.add((restriction_brand, RDF.type, OWL.Restriction))
        g1.add((restriction_brand, OWL.onProperty, homex.hasBrand))
        g1.add((restriction_brand, OWL.hasValue, URIRef(brand_uri)))
    else:
        pass

    restriction_modelno = BNode()
    if(not pd.isna(model_number)):
        g1.add((restriction_modelno, RDF.type, OWL.Restriction))
        g1.add((restriction_modelno, OWL.onProperty, homex.hasModelNumber))
        g1.add((restriction_modelno, OWL.hasValue, URIRef(model_number_uri)))
    else:
        pass

    restriction_problem = BNode()
    if(not pd.isna(problem)):
        g1.add((restriction_problem, RDF.type, OWL.Restriction))
        g1.add((restriction_problem, OWL.onProperty, homex.hasProblem))
        g1.add((restriction_problem, OWL.someValuesFrom, URIRef(problem_uri)))
    else:
        pass




###### Subject Construction ######

    subject_collection_items = [
        homex.Refrigerator,
        restriction_problem,
        restriction_modelno,
        restriction_brand ]
    
    subject_non_empty_restrictions = []
    for item in subject_collection_items:
        if is_empty_blank_node(graph=g1, blank_node=item):
            continue  # Skip empty items
        subject_non_empty_restrictions.append(item)

    
    if subject_non_empty_restrictions:
        subject_intersection_node = BNode()
        subject_intersection_list = BNode()
        g1.add((subject_intersection_node, RDF.type, OWL.Class))
        g1.add((subject_intersection_node, OWL.intersectionOf, subject_intersection_list))


        for index, item in enumerate(subject_non_empty_restrictions):
            g1.add((subject_intersection_list, RDF.first, item))
            if index < len(subject_non_empty_restrictions) - 1:
                next_item = BNode()
                g1.add((subject_intersection_list, RDF.rest, next_item))
                subject_intersection_list = next_item
            else:
                g1.add((subject_intersection_list, RDF.rest, RDF.nil))



    ###### Connect subject and object ######
    g1.add((URIRef(artefact_uri), RDF.type, OWL.Class))
    g1.add((URIRef(artefact_uri), OWL.equivalentClass, subject_intersection_node))

    if symptom_uri is not None:
        g1.add((URIRef(artefact_uri), homex.hasSymptom, URIRef(symptom_uri)))
    if investigation_uri is not None:
        g1.add((URIRef(artefact_uri), homex.hasInvestigation, URIRef(investigation_uri)))
    if investigation_equipment_uri is not None:
        g1.add((URIRef(artefact_uri), homex.hasInvestigationEquipment, URIRef(investigation_equipment_uri)))
    if resolution_uri is not None:
        g1.add((URIRef(artefact_uri), homex.hasResolution, URIRef(resolution_uri)))
    if resolution_equipment_uri is not None:
        g1.add((URIRef(artefact_uri), homex.hasResolutionEquipment, URIRef(resolution_equipment_uri)))
    if resolution_manner_uri is not None:
        g1.add((URIRef(artefact_uri), homex.hasResolutionMannerAttribute, URIRef(resolution_manner_uri)))


# Serialize the graph to a Turtle file
turtle_file = "Ontology_Mapping/Mapping_Test.ttl"
g1.serialize(destination=turtle_file, format="turtle", encoding="utf-8")


kg = kglab.KnowledgeGraph()
kg.load_rdf("Ontology_Mapping/Mapping_Test.ttl", format="turtle")


output_folder = "/Users/cenxitoh/Desktop/Project_Python/Ontology_Mapping/Archived/"
kg.save_parquet(output_folder + "Mapping_Test.parquet")
full_df = pd.read_parquet(output_folder + "Mapping_Test.parquet")


def get_last_fragment(uri):
    return uri.rsplit("#", 1)[-1][:-1] if "#" in uri else uri.rsplit("/", 1)[-1][:-1]

# Apply the function to the subject, predicate, and object columns
full_df["subject"] = full_df["subject"].apply(get_last_fragment)
full_df["predicate"] = full_df["predicate"].apply(get_last_fragment)
full_df["object"] = full_df["object"].apply(get_last_fragment)


full_df.to_csv('Ontology_Mapping/Mapping_Test.txt' , sep="\t", index=False)
full_df.to_csv('Ontology_Mapping/Mapping_Test.csv', index=False)