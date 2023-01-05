from typing import List
import streamlit as st
from streamlit_searchbox import st_searchbox
from elasticsearch import Elasticsearch


client = Elasticsearch(
    "https://localhost:9200",
    ca_certs=f"C:/Users/dehab/Downloads/elasticsearch-8.5.3/config/certs/http_ca.crt",
    basic_auth=("elastic", "uN5jJVipsKVYiJLxYZND")
)


def search_(searchterm) -> List[str]:
    query_body = {      
    "query": {
        "bool": {
            "must": [
                    {
                    "match_phrase_prefix": {
                        "title": {
                            "query": "{}".format(f"{searchterm}")}
                            }
                        }
                    ],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "title.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 25}}}
                        }
        
    synonym_query = {"query" : {"match_phrase" : {"title" : {
               "query" : "",
               "analyzer": "synonym_analyzer"
            }}}}

    res = client.search(index="sha_autofill", body=query_body)
    return_list = []

    for i in res["hits"]["hits"]:
        return_list.append(i["_source"]["title"])
        synonym_query["query"]["match_phrase"]["title"]["query"] = i["_source"]["title"]
        res_syn = client.search(index="sha_autofill", body=synonym_query)
        data = res_syn["hits"]["hits"][0]["_source"]["title"]
        if data is not None and data not in return_list:
            return_list.append(data)
    return return_list

def main():
    st.set_page_config(page_title="Example App", page_icon="🤖")
    st.title("Get Title")

    selected_value = st_searchbox(
        search_,
        key="wiki_searchbox",
    )

    st.markdown("You've selected: %s" % selected_value)


if __name__ == '__main__':
    main()