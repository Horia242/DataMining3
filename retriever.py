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

    with open("new_questions.txt", "r") as file:
        lines = file.readlines()

    correct_count = 0
    total_count = 0

    for i in range(0, len(lines), 4):
        category = lines[i].strip()
        query = lines[i+1].strip()
        expected_result = lines[i+2].strip()

        result = retrieve_best_page(index, query, category)

        print(f"Category: {category}")
        print(f"Query: {query}")
        print(f"Expected Result: {expected_result}")

        total_count += 1
        if result == expected_result:
            print(f"Result: {result} - Correct!")
            correct_count += 1
        else:
            print(f"Result: {result} - Incorrect!")

        print("=" * 40)

    print(f"\nP@1: {(correct_count/total_count)*100}%")
