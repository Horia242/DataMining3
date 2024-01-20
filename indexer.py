from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
import os

def create_index(schema, index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    index = create_in(index_dir, schema)
    return index

def index_wikipedia_data(index, data_folder):
    writer = index.writer()
    k = 0
    for file_name in os.listdir(data_folder):
        k = k + 1
        print(f"Processing file: {file_name}")
        print(k)
        with open(os.path.join(data_folder, file_name), 'r', encoding='latin-1') as file:
            content = file.read()
            articles = content.split('[[')[1:]  # Split the content into articles
            for article in articles:
                title_end = article.find(']]')
                title = article[:title_end].strip()
                text = article[title_end + 2:].strip()
                writer.add_document(title=title, content=text)

    writer.commit()

if __name__ == "__main__":
    schema = Schema(title=ID(stored=True), content=TEXT)
    index_dir = "index"
    data_folder = "wikipediaDataMining"

    index = create_index(schema, index_dir)
    index_wikipedia_data(index, data_folder)
