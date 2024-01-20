from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir

def retrieve_best_page(index, query, category=None):
    searcher = index.searcher(weighting=scoring.TF_IDF())
    parser = QueryParser("content", schema=index.schema)

    if category:
        query = f"{category} {query}"

    q = parser.parse(query)
    results = searcher.search(q, limit=1)

    if results:
        return results[0]['title']
    else:
        return None


if __name__ == "__main__":
    index_dir = "index"

    index = open_dir(index_dir)

    query = "The name of this largest Moroccan city combines 2 Spanish words"
    category = "AFRICAN CITIES"

    result = retrieve_best_page(index, query, category)

    if result:
        print(f"The best matching Wikipedia page is: {result}")
    else:
        print("No matching page found.")
