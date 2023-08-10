from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD
import pandas as pd
import csv

# Create an RDF graph
g1 = Graph()

# Load data from a Turtle file
turtle_file = "CUNO_script.ttl"
g1.parse(turtle_file, format="turtle")

homex = Namespace("http://example.org/homex#")
g1.bind("homex",homex)

df = pd.read_csv('SyntheticData.csv')

#########################################################################################
# Map the UDT to the CUNO_script created earlier

for quantity, artefact, brand, model_number, problem, symptom, investigation, investigation_equipment, resolution, resolution_manner, resolution_equipment in zip(df['Quantity'],df['Artefact'],df['Brand'],df['Model Number'],df['Artefact Problem'],df['Problem Symptoms'],df['Problem Investigation'],df['Artefacts Needed for Problem Investigation'],df['Problem Resolution'],df['Way of Carrying Out the Problem Resolution'],df['Artefacts Needed for Problem Resolution']):

    ##Create URIs

    #Artefact
    artefact_uri = homex + artefact.lower() + "/" + brand + "/" + str(model_number) + "/" + problem.lower().replace(" ","_")
    #g1.add((URIRef(artefact_uri), RDFS.subClassOf, homex.Artefact))

    #Problem    
    problem_uri = homex + problem.lower().replace(" ","_")
    g1.add((URIRef(problem_uri), RDF.type, homex.Issue))

    #Brand
    if(not pd.isna(brand)):
        brand_uri = homex + brand
        g1.add((URIRef(brand_uri), RDF.type, homex.Brand))
        
    #ModelNumber
    if(not pd.isna(model_number)):
        model_number_uri = homex + str(model_number)
        g1.add((URIRef(model_number_uri), RDF.type, homex.ModelNumber))

    #Symptom    
    if(not pd.isna(symptom)):
        symptom_uri = homex + str(symptom).lower().replace(" ","_")
        g1.add((URIRef(symptom_uri), RDF.type, homex.Issue))

    #Investigation 
    if(not pd.isna(investigation)):   
        investigation_uri = homex + str(investigation).lower().replace(" ","_")
        g1.add((URIRef(investigation_uri), RDF.type, homex.Investigation))
    
    #Investigation Equipment
    if(not pd.isna(investigation_equipment)):
        investigation_equipment_uri = homex + str(investigation_equipment).lower().replace(" ","_")
        g1.add((URIRef(investigation_equipment_uri), RDF.type, homex.Sort))

    #Resolution    
    if(not pd.isna(resolution)):
        resolution_uri = homex + str(resolution).lower().replace(" ","_")
        g1.add((URIRef(resolution_uri), RDF.type, homex.Resolution))

    #Resolution Manner   
    if(not pd.isna(resolution_manner)): 
        resolution_manner_uri = homex + str(resolution_manner).lower().replace(" ","_")
        g1.add((URIRef(resolution_manner_uri), RDF.type, homex.MannerAttribute))

    #Resolution Equipment  
    if(not pd.isna(resolution_equipment)):  
        resolution_equipment_uri = homex + str(resolution_equipment).lower().replace(" ","_")
        g1.add((URIRef(resolution_equipment_uri), RDF.type, homex.Sort))






    #Create restrictions for each attribute

    restriction_brand = BNode()
    if (not pd.isna(brand)):
        g1.add((restriction_brand, RDF.type, OWL.Restriction))
        g1.add((restriction_brand, OWL.onProperty, homex.hasBrand))
        g1.add((restriction_brand, OWL.hasValue, URIRef(brand_uri)))

    restriction_modelno = BNode()
    if(not pd.isna(model_number)):
        g1.add((restriction_modelno, RDF.type, OWL.Restriction))
        g1.add((restriction_modelno, OWL.onProperty, homex.hasModelNumber))
        g1.add((restriction_modelno, OWL.hasValue, URIRef(model_number_uri)))

    restriction_symptom = BNode()
    if(not pd.isna(symptom)):
        g1.add((restriction_symptom, RDF.type, OWL.Restriction))
        g1.add((restriction_symptom, OWL.onProperty, homex.hasSymptom))
        g1.add((restriction_symptom, OWL.someValuesFrom, URIRef(symptom_uri)))

    restriction_investigation = BNode()
    if(not pd.isna(investigation)):
        g1.add((restriction_investigation, RDF.type, OWL.Restriction))
        g1.add((restriction_investigation, OWL.onProperty, homex.hasInvestigation))
        g1.add((restriction_investigation, OWL.hasValue, URIRef(investigation_uri)))

    restriction_invequip = BNode()
    if(not pd.isna(investigation_equipment)):
        g1.add((restriction_invequip, RDF.type, OWL.Restriction))
        g1.add((restriction_invequip, OWL.onProperty, homex.hasInvestigationEquipment))
        g1.add((restriction_invequip, OWL.hasValue, URIRef(investigation_equipment_uri)))

    restriction_resolution = BNode()
    if(not pd.isna(resolution)):
        g1.add((restriction_resolution, RDF.type, OWL.Restriction))
        g1.add((restriction_resolution, OWL.onProperty, homex.hasResolution))
        g1.add((restriction_resolution, OWL.hasValue, URIRef(resolution_uri)))

    restriction_resequip = BNode()
    if(not pd.isna(resolution_equipment)):
        g1.add((restriction_resequip, RDF.type, OWL.Restriction))
        g1.add((restriction_resequip, OWL.onProperty, homex.hasResolutionEquipment))
        g1.add((restriction_resequip, OWL.hasValue, URIRef(resolution_equipment_uri)))

    restriction_resmanner = BNode()
    if(not pd.isna(resolution_manner)):
        g1.add((restriction_resmanner, RDF.type, OWL.Restriction))
        g1.add((restriction_resmanner, OWL.onProperty, homex.hasResolutionMannerAttribute))
        g1.add((restriction_resmanner, OWL.hasValue, URIRef(resolution_manner_uri)))

    restriction_problem = BNode()
    if(not pd.isna(problem)):
        g1.add((restriction_problem, RDF.type, OWL.Restriction))
        g1.add((restriction_problem, OWL.onProperty, homex.hasProblem))
        g1.add((restriction_problem, OWL.someValuesFrom, URIRef(problem_uri)))

 


    # Subject construction (Artefact, Brand, Model Number, Problem)
    intersection_node = BNode()
    restriction_node = BNode()

    g1.add((URIRef(artefact_uri), RDF.type, OWL.Class))
    g1.add((URIRef(artefact_uri), OWL.equivalentClass, intersection_node))
    g1.add((intersection_node, RDF.type, OWL.Class))
    g1.add((intersection_node, OWL.intersectionOf, homex.Refrigerator))
    g1.add((intersection_node, OWL.intersectionOf, restriction_brand))
    g1.add((intersection_node, OWL.intersectionOf, restriction_modelno))
    g1.add((intersection_node, OWL.intersectionOf, restriction_problem))



    # Object construction (Symptoms, Investigation, Resolution)
    restriction_problem2 = BNode()
    intersection_node2 = BNode()

    if(not pd.isna(problem)):
        g1.add((restriction_problem2, RDF.type, OWL.Class))##
        g1.add((restriction_problem2, OWL.onProperty, homex.hasProblem))
        g1.add((restriction_problem2, OWL.intersectionOf, homex.Issue))
        g1.add((restriction_problem2, OWL.intersectionOf, restriction_symptom))
        g1.add((restriction_problem2, OWL.intersectionOf, restriction_investigation))
        g1.add((restriction_problem2, OWL.intersectionOf, restriction_invequip))
        g1.add((restriction_problem2, OWL.intersectionOf, restriction_resolution))
        g1.add((restriction_problem2, OWL.intersectionOf, restriction_resequip))
        g1.add((restriction_problem2, OWL.intersectionOf, restriction_resmanner))

    g1.add((URIRef(artefact_uri), RDFS.subClassOf, restriction_problem2))


#########################################################################################

# Serialize the graph to a Turtle file
turtle_file = "UDT_mapping.ttl"
g1.serialize(destination=turtle_file, format="turtle", encoding="utf-8")