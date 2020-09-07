def query_definition(search_query):
    if search_query:
        return {
            "multi_match": {
                "query": search_query,
                "fields": ["title", "description", "writers_names", "actors_names", "director"]
            }
        }

    return {"match_all": {}}