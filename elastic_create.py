from elasticsearch import Elasticsearch, helpers

class Elastic_Create:
    def __init__(self) -> None:
        self.client = Elasticsearch("https://localhost:9200",
                            ca_certs=f"C:/Users/dehab/Downloads/elasticsearch-8.5.3/config/certs/http_ca.crt",
                            basic_auth=("elastic", "uN5jJVipsKVYiJLxYZND")
                            )
        self.synonyms = []
        self.words = []
        self.index_settings = {
                            "settings": {
                                "analysis": {
                                    "analyzer": {
                                    "synonym_analyzer": {
                                        "tokenizer": "whitespace",
                                        "filter": ["lowercase", "my_synonyms"]
                                    }
                                    },
                                    "filter": {
                                    "my_synonyms": {
                                        "type": "synonym",
                                        "synonyms": self.synonyms
                                    }
                                    }
                                }
                            }
                            }

    def create_index(self, index_name: str):
        self.client.indices.create(index=index_name, body=self.index_settings)

    def insert_index(self, index_name: str):
        new_id = []
        for i in range(0, len(self.words)):
            new_id.append(i)

        def gendata(new_id):
            for i in range(len(new_id)):
                yield {
                    "_index": f"{index_name}",
                    "_id":new_id[i],
                    "title": self.words[i],
                }
        
        helpers.bulk(self.client,gendata(new_id))


if __name__ == '__main__':
    body = ["sap human resources consultant => sap hr consultant", 
            "sap hr consultant => sap human resources consultant",
            "sap epm consultant => sap enterprise performance management consultant",
            "sap enterprise performance management consultant => sap epm consultant",
            "sap mm consultant => sap material management consultant",
            "sap material management consultant => sap mm consultant"]

    words = [
            "sap human resources consultant",
            "sap hr consultant",
            "sap epm consultant",
            "sap enterprise performance management consultant" ,
            "sap mm consultant",
            "sap material management consultant",
            "sap sales And distribution consultant",
            "sap sd consultant",
            "sap transportation management consultaant",
            "sap tm consultant",
            "sap human capital management consultant",
            "sap hcm consultant",
            "sap ewm consultant"
            "sap extended warehouse management consultant" ,
            "sap financial consultant",
            "sap fi consultant",
            "sap pp consultant",
            "sap pm consultant",
            "sap production planinng consultant",
            "sap plant maintenance consultant",
            "sap quality management consultant",
            "sap qm consultant",
            "sap ps consultant",
            "sap project systems consultant",
            "sap co consultant",
            "sap controlling consultant"]

    elastic = Elastic_Create()
    elastic.synonyms = body
    elastic.words = words
    
    elastic.create_index(index_name="sha_autocomplete")
    elastic.insert_index(index_name="sha_autocomplete")
