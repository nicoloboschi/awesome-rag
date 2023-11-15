import csv

from langchain.schema.vectorstore import VectorStore

from recommendations.recommendations.setup import create_astra_vector_store


def index(vector: VectorStore):

    texts = []
    metadatas = []
    ids = []
    with open("./products.csv") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for i, row in enumerate(csv_reader):
            texts.append(row["DESCRIPTION"])
            metadatas.append(row)
            ids.append(i)
    vector.add_texts(texts, metadatas, ids=ids)

def main():

    collection_name = "recs1"
    astra_vector_store = create_astra_vector_store(collection_name)

    index(astra_vector_store)
    print(astra_vector_store.astra_db.collection("recs").find())

if __name__ == '__main__':
    main()
