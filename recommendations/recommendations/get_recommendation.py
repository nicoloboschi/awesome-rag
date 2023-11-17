import json
import os
from operator import itemgetter
from typing import Sequence

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser, Document
from langchain.schema.runnable import RunnableMap, RunnableLambda
from langchain.vectorstores import AstraDB

from recommendations.recommendations.util import create_astra_vector_store, get_openai_token, USERS_COLLECTION_NAME, \
    PRODUCTS_COLLECTION_NAME

RESPONSE_TEMPLATE = """
You are a helpful assistant.
The user is looking for buying a complimentary product of: "{product}". 
Create a recommendation of 1 to 4 products to buy specifically for the user.
If you don't think the user should buy anything, just not list any product.  
Each `item` in the following `products` html blocks, is a possible product to recommend. Do not make up products not listed here. \

<products>
  {possible_products}
<products/>

{user_info}



For each product recommended, add a field explaining why you think they would buy those product
Also include a short comparison between it and the similar product mentioned earlier. 
Keep it in less than 50 words.
Export the results in a JSON List format. 
The top level object is a list. 
Each item has a "product_info" field - as json object - containing the 'metadata' field content provided in the `<product>` html tag - so please parse it from JSON -
and a "reason" field containing the reason.
"""


def main():
    print("using collection: " + PRODUCTS_COLLECTION_NAME)
    astra_vector_store = create_astra_vector_store(PRODUCTS_COLLECTION_NAME)
    retriever = astra_vector_store.as_retriever()

    def user_info(user):
        user_info = astra_vector_store.astra_db.collection(USERS_COLLECTION_NAME).find_one({
            "handle": user,
        })
        if user_info["data"]["document"]:
            return f"""
            Additionally, In the following JSON object there are some information about the user that you can use to make the recommendation.
            {json.dumps({
                "first_name": user_info["data"]["document"]["first_name"],
                "last_name": user_info["data"]["document"]["last_name"],
                "age": user_info["data"]["document"]["age"],
                "gender": user_info["data"]["document"]["gender"],
            })}
            """
        return ""

    def format_possible_products(docs: Sequence[Document]) -> str:
        formatted_docs = []
        for doc in enumerate(docs):
            actual_doc = doc[1]
            metadata = json.dumps(actual_doc.metadata)

            doc_string = f"<product metadata='{metadata}'>{actual_doc.page_content}</product>"
            formatted_docs.append(doc_string)
        return "\n".join(formatted_docs)

    def format_response(text):
        return json.loads(text)

    llm = ChatOpenAI(
        openai_api_key=get_openai_token(),
        model="gpt-3.5-turbo-16k",
        streaming=True,
        temperature=0,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", RESPONSE_TEMPLATE)
        ]
    )
    chain = (prompt | llm | StrOutputParser() | RunnableLambda(format_response)).with_config(
        run_name="GenerateResponse",
    )

    retrieve_chain = RunnableMap(
        {
            "product": itemgetter("product"),
            "possible_products": itemgetter("product") | retriever | format_possible_products,
            "user_info": itemgetter("user") | RunnableLambda(user_info)
        }
    ).with_config(run_name="RetrieveDocs")

    while True:
        user = input("User handle? ['max', 'adele']\n")
        product = input("Product?\n")
        response = (
                retrieve_chain | chain
        ).invoke({
            "product": product,
            "user": user
        })
        print("\nSuggested products:\n")
        for suggested in response:
            print(suggested["product_info"]["NAME"] + " - " + suggested["product_info"]["PRICE"] + "$. " + suggested[
                "reason"])
        print("\n")


if __name__ == '__main__':
    main()
