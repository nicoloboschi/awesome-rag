import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.embeddings import Embeddings
from langchain.vectorstores.astradb import AstraDB
from astrapy.db import (
                AstraDB as LibAstraDB,
)
from astrapy.db import (
                AstraDBCollection as LibAstraDBCollection,
)

def get_openai_token() -> str:
    return os.getenv("OPENAI_API_KEY",
                     "")


def create_astra_vector_store(collection: str) -> AstraDB:
    return AstraDB(
        collection_name=collection,
        embedding=OpenAIEmbeddings(openai_api_key=get_openai_token()),
        token=os.getenv("ASTRA_DB_TOKEN",
                        ""),
        api_endpoint=os.getenv("ASTRA_DB_ENDPOINT",
                               "")
    )


def create_raw_astra_client() -> LibAstraDB:
    return LibAstraDB(
        token=get_astra_token(),
        api_endpoint=get_astra_api_endpoint()
    )


def get_astra_api_endpoint():
    return os.getenv("ASTRA_DB_ENDPOINT",
                     "")


def get_astra_token():
    return os.getenv("ASTRA_DB_TOKEN",
                     "")



if __name__ == '__main__':
    # create users table
    create_astra_vector_store("recs1").astra_db.collection("recs1").find_one()

    astra_db = create_raw_astra_client()
    #astra_db.create_collection(collection_name="users")
    print(astra_db.collection("users").insert_one({"first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "gender": "male"
    }))
