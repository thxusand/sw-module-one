from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

sparql.setQuery("""
    SELECT ?disease ?diseaseLabel ?diagnosis ?diagnosisLabel
    WHERE {
      ?disease rdf:type dbo:Disease ;
               dbo:wikiPageWikiLink dbr:Gastroenterology .
               
      OPTIONAL { ?disease dbo:diagnosis ?diagnosis .
            ?diagnosis rdfs:label ?diagnosisLabel .
            FILTER (lang(?diagnosisLabel) = "en") }
      
      OPTIONAL { ?disease dbp:diagnosis ?diagnosisAlt .
             ?diagnosisAlt rdfs:label ?diagnosisLabelAlt .
             FILTER (lang(?diagnosisLabelAlt) = "en") }

      OPTIONAL { ?disease dbo:medicalProcedure ?medicalProcedure .
             ?medicalProcedure rdfs:label ?procedureLabel .
             FILTER (lang(?procedureLabel) = "en") }
    
      ?disease rdfs:label ?diseaseLabel . 
      FILTER (lang(?diseaseLabel) = "en")
    }
    LIMIT 50
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

graph = Graph()

for result in results["results"]["bindings"]:
    disease = result["disease"]["value"]
    diagnosis_method = result.get("diagnosisMethod", {}).get("value", "N/A")

    graph.add((URIRef(disease), URIRef("http://example.org/hasDiagnosisMethod"), Literal(diagnosis_method)))

    print(f"Disease: {disease}, Diagnosis Method: {diagnosis_method}")

graph.serialize("gastroenterology_diseases_extended.ttl", format="json-ld")