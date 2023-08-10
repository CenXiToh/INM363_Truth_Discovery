#CUNO
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD
import pandas as pd
import csv

g1 = Graph()

homex = Namespace("http://example.org/homex#")
g1.bind("homex",homex)



#########################################################################################
#CREATE CUNO STRUTURE

# Individual
g1.add((homex.Individual, RDF.type, OWL.Class))
g1.add((homex.Individual, RDF.type, homex.Kind))
g1.add((homex.Individual, RDFS.subClassOf, OWL.Thing))
    
g1.add((homex.Mode, RDF.type, OWL.Class))
g1.add((homex.Mode, RDF.type, homex.Kind))
g1.add((homex.Mode, RDFS.subClassOf, homex.Individual))
    
g1.add((homex.Issue, RDF.type, OWL.Class))
g1.add((homex.Issue, RDFS.subClassOf, homex.Mode))
    
g1.add((homex.Manner, RDF.type, OWL.Class))
g1.add((homex.Manner, RDFS.subClassOf, homex.Mode))
    
g1.add((homex.Response, RDF.type, OWL.Class))
g1.add((homex.Response, RDFS.subClassOf, homex.Mode))
    
g1.add((homex.Investigation, RDF.type, OWL.Class))
g1.add((homex.Investigation, RDFS.subClassOf, homex.Response))
    
g1.add((homex.Resolution, RDF.type, OWL.Class))
g1.add((homex.Resolution, RDFS.subClassOf, homex.Response)) 
    
g1.add((homex.Object, RDF.type, OWL.Class))
g1.add((homex.Object, RDF.type, homex.Kind))
g1.add((homex.Object, RDFS.subClassOf, homex.Individual))
    
g1.add((homex.Artefact, RDF.type, OWL.Class))
g1.add((homex.Artefact, RDF.type, homex.Sort))
g1.add((homex.Artefact, RDF.type, homex.Kind))
g1.add((homex.Artefact, RDFS.subClassOf, homex.Object))
g1.add((homex.Refrigerator, RDFS.subClassOf, homex.Artefact))
    
    
#Class
    
g1.add((OWL.Class, RDF.type, homex.Kind))
g1.add((OWL.Class, RDFS.subClassOf, OWL.Thing))

g1.add((homex.Kind, RDF.type, OWL.Class))
g1.add((homex.Kind, RDF.type, homex.Kind))
g1.add((homex.Kind, RDFS.subClassOf, OWL.Class))
    
g1.add((homex.Attribute, RDF.type, OWL.Class))
g1.add((homex.Attribute, RDF.type, homex.Kind))
g1.add((homex.Attribute, RDFS.subClassOf, homex.Kind))
    
g1.add((homex.Brand, RDF.type, OWL.Class))
g1.add((homex.Brand, RDFS.subClassOf, homex.Attribute))
    
g1.add((homex.ModelNumber, RDF.type, OWL.Class))
g1.add((homex.ModelNumber, RDFS.subClassOf, homex.Attribute))
    
g1.add((homex.MannerAttribute, RDF.type, OWL.Class))
g1.add((homex.MannerAttribute, RDFS.subClassOf, homex.Attribute))
    
g1.add((homex.Sort, RDF.type, OWL.Class))
g1.add((homex.Sort, RDF.type, homex.Kind))
g1.add((homex.Sort, RDFS.subClassOf, homex.Kind))
    
g1.add((homex.MereClass, RDF.type, OWL.Class))
g1.add((homex.MereClass, RDF.type, homex.Kind))
g1.add((homex.MereClass, RDFS.subClassOf, OWL.Class))


#owl:thing is also a kind:
g1.add((OWL.Thing, RDF.type, homex.Kind))


#########################################################################################
# OBJECT PROPERTIES

#hasAttribute
g1.add((homex.hasAttribute, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasAttribute, RDFS.domain, OWL.Thing))
g1.add((homex.hasAttribute, RDFS.range, homex.Attribute))
g1.add((homex.hasAttribute, OWL.inverseOf, homex.isAttributeOf))

#isAttributeOf
g1.add((homex.isAttributeOf, RDF.type, OWL.ObjectProperty))

#hasBrand
g1.add((homex.hasBrand, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasBrand, RDFS.domain, homex.Artefact))
g1.add((homex.hasBrand, RDFS.range, homex.Attribute))
g1.add((homex.hasBrand, RDFS.subPropertyOf, homex.hasAttribute))
g1.add((homex.hasBrand, OWL.inverseOf, homex.isBrandOf))

#isBrandOf
g1.add((homex.isBrandOf, RDF.type, OWL.ObjectProperty))
g1.add((homex.isBrandOf, RDFS.subPropertyOf, homex.isAttributeOf))

#hasModelNumber
g1.add((homex.hasModelNumber, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasModelNumber, RDFS.domain, homex.Artefact))
g1.add((homex.hasModelNumber, RDFS.range, homex.Attribute))
g1.add((homex.hasModelNumber, RDFS.subPropertyOf, homex.hasAttribute))
g1.add((homex.hasModelNumber, OWL.inverseOf, homex.isModelNumberOf))

#isModelNumberOf
g1.add((homex.isModelNumberOf, RDF.type, OWL.ObjectProperty))
g1.add((homex.isModelNumberOf, RDFS.subPropertyOf, homex.isAttributeOf))

#hasParticipant
g1.add((homex.hasParticipant, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasParticipant, RDFS.domain, homex.Mode))
g1.add((homex.hasParticipant, RDFS.range, OWL.Thing))
g1.add((homex.hasParticipant, OWL.inverseOf, homex.isParticipantOf))

#isParticipantOf
g1.add((homex.isParticipantOf, RDF.type, OWL.ObjectProperty))

#hasBearer
g1.add((homex.hasBearer, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasBearer, RDFS.domain, homex.Mode))
g1.add((homex.hasBearer, RDFS.range, OWL.Thing))
g1.add((homex.hasBearer, RDFS.subPropertyOf, homex.hasParticipant))
g1.add((homex.hasBearer, OWL.inverseOf, homex.isBearerOf))

#isBearerOf
g1.add((homex.isBearerOf, RDF.type, OWL.ObjectProperty))
g1.add((homex.isBearerOf, RDFS.subPropertyOf, homex.isParticipantOf))

#hasIssue
g1.add((homex.hasIssue, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasIssue, RDFS.domain, homex.Artefact))
g1.add((homex.hasIssue, RDFS.range, homex.Issue))
g1.add((homex.hasIssue, OWL.inverseOf, homex.isIssueOf))

#isIssueOf
g1.add((homex.isIssueOf, RDF.type, OWL.ObjectProperty))

#hasProblem
g1.add((homex.hasProblem, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasProblem, RDFS.domain, homex.Artefact))
g1.add((homex.hasProblem, RDFS.range, homex.Issue))
g1.add((homex.hasProblem, RDFS.subPropertyOf, homex.hasIssue))
g1.add((homex.hasProblem, OWL.inverseOf, homex.isProblemOf))

#isProblemOf
g1.add((homex.isProblemOf, RDF.type, OWL.ObjectProperty))

#hasSymptom
g1.add((homex.hasSymptom, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasSymptom, RDFS.domain, homex.Issue))
g1.add((homex.hasSymptom, RDFS.range, homex.Issue))
g1.add((homex.hasSymptom, RDFS.subPropertyOf, homex.hasIssue))
g1.add((homex.hasSymptom, OWL.inverseOf, homex.isSymptomOf))

#isSymptomOf
g1.add((homex.isSymptomOf, RDF.type, OWL.ObjectProperty))

#hasInvestigation
g1.add((homex.hasInvestigation, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasInvestigation, RDFS.domain, homex.Issue))
g1.add((homex.hasInvestigation, RDFS.range, homex.Attribute))
g1.add((homex.hasInvestigation, OWL.inverseOf, homex.isInvestigationOf))

#isInvestigationOf
g1.add((homex.IsInvestigationOf, RDF.type, OWL.ObjectProperty))

#hasInvestigationEquipment
g1.add((homex.hasInvestigationEquipment, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasInvestigationEquipment, OWL.inverseOf, homex.isInvestigationEquipmentOf))
g1.add((homex.hasInvestigationEquipment, RDFS.domain, homex.Issue))
g1.add((homex.hasInvestigationEquipment, RDFS.range, homex.Sort))

#isInvestigationEquipmentOf
g1.add((homex.isInvestigationEquipmentOf, RDF.type, OWL.ObjectProperty))

#hasResolution
g1.add((homex.hasResolution, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasResolution, RDFS.domain, homex.Issue))
g1.add((homex.hasResolution, RDFS.range, homex.Attribute))
g1.add((homex.hasResolution, OWL.inverseOf, homex.isResolutionOf))

#isResolutionOf
g1.add((homex.isResolutionOf, RDF.type, OWL.ObjectProperty))

#hasResolutionEquipment
g1.add((homex.hasResolutionEquipment, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasResolutionEquipment, OWL.inverseOf, homex.isResolutionEquipmentOf))
g1.add((homex.hasResolutionEquipment, RDFS.domain, homex.Issue))
g1.add((homex.hasResolutionEquipment, RDFS.range, homex.Sort))

#isResolutionEquipmentOf
g1.add((homex.isResolutionEquipmentOf, RDF.type, OWL.ObjectProperty))

#hasMannerAttribute
g1.add((homex.hasMannerAttribute, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasMannerAttribute, RDFS.domain, homex.Issue))
g1.add((homex.hasMannerAttribute, RDFS.range, homex.MannerAttribute))
g1.add((homex.hasMannerAttribute, OWL.inverseOf, homex.isMannerAttributeOf))

#isMannerAttributeOf
g1.add((homex.isMannerAttributeOf, RDF.type, OWL.ObjectProperty))

#hasResolutionMannerAttribute
g1.add((homex.hasResolutionMannerAttribute, RDF.type, OWL.ObjectProperty))
g1.add((homex.hasResolutionMannerAttribute, RDFS.domain, homex.Issue))
g1.add((homex.hasResolutionMannerAttribute, RDFS.range, homex.MannerAttribute))
g1.add((homex.hasResolutionMannerAttribute, RDFS.subPropertyOf, homex.hasMannerAttribute))
g1.add((homex.hasResolutionMannerAttribute, OWL.inverseOf, homex.isResolutionMannerAttributeOf))

#isResolutionMannerAttributeOf
g1.add((homex.isResolutionMannerAttributeOf, RDF.type, OWL.ObjectProperty))
g1.add((homex.isResolutionMannerAttributeOf, RDFS.subPropertyOf, homex.isMannerAttributeOf))


#########################################################################################
# Serialize the graph to a Turtle file
turtle_file = "CUNO_script.ttl"
g1.serialize(destination=turtle_file, format="turtle", encoding="utf-8")