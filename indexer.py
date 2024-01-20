from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
import os
import re

def create_index(schema, index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    index = create_in(index_dir, schema)
    return index

def extract_title_and_text(content):
    # Use a regular expression to extract title and text
    match = re.search(r'\[\[(.+?)\]\]\s*([\s\S]*)', content)
    if match:
        title, text = match.groups()
        return title.strip(), text.strip()
    return None, None

def index_wikipedia_data(index, data_folder):
    writer = index.writer()

    for file_name in os.listdir(data_folder):
        with open(os.path.join(data_folder, file_name), 'r', encoding='UTF-8') as file:
            content = file.read()

            # Extract title and text
            title, text = extract_title_and_text(content)

            if title and text:
                # Add document to the index
                writer.add_document(title=title, content=text)

    writer.commit()

if __name__ == "__main__":
    schema = Schema(title=ID(stored=True), content=TEXT)
    index_dir = "index"
    data_folder = "wikipediaDataMining"

    index = create_index(schema, index_dir)
    index_wikipedia_data(index, data_folder)