from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

sparql.setQuery("""
    SELECT ?disease ?diagnosis ?symptoms WHERE {
        ?disease dbo:wikiPageWikiLink dbc:Gastroenterology ;
                 rdf:type dbo:Disease .
        OPTIONAL { ?disease dbo:medicalDiagnosis ?diagnosis }
    }
    LIMIT 50
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

graph = Graph()

for result in results["results"]["bindings"]:
    disease = result["disease"]["value"]
    diagnosis = result.get("diagnosis", {}).get("value", "Not available")
    symptoms = result.get("symptoms", {}).get("value", "Not available")

    graph.add((URIRef(disease), URIRef("http://example.org/hasDiagnosisMethod"), Literal(diagnosis)))
    print(f"Disease: {disease}, Diagnosis Method: {diagnosis}")

graph.serialize("gastroenterology_diseases.ttl", format="json-ld")
