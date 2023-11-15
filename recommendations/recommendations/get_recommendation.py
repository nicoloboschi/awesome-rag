import os
from operator import itemgetter

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnableLambda
from langchain.vectorstores import AstraDB

from recommendations.recommendations.setup import create_astra_vector_store, get_openai_token

RESPONSE_TEMPLATE = """
You are a helpful assistant.
The user is looking for buying a complimentary product of: "{question}". 
Create a recommendation of 1 to 4 products to buy specifically for the user.
If you don't think the user should buy anything, just not list any product.  
Each `item` in the following `products` html blocks, is a possible product to recommend. Do not make up products not listed here. \

<products>
  {context}
<products/>

Additionally, In the following `user` html block there are some information about the user that you can use to make the recommendation.
<user>
Name: John
Age: 30
Gender: Male
</user>


For each product recommended, add a field explaining why you think they would buy those product
Also include a short comparison between it and the similar product mentioned earlier. 
Keep it in less than 50 words.
Export the results in a JSON List format. 
The top level object is a list. 
Each item has a "product" field containing the product name and a "reason" field containing the reason. 
"""

def main():
    astra_vector_store = create_astra_vector_store("recs1")
    retriever = astra_vector_store.as_retriever()

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
    chain = (prompt | llm | StrOutputParser()).with_config(
        run_name="GenerateResponse",
    )

    retrieve_chain = RunnableMap(
        {
            "question": itemgetter("product"),
            "context": itemgetter("product") | retriever
        }
    ).with_config(run_name="RetrieveDocs")

    user = input("User handle?\n")
    while True:
        product = input("Product?\n")
        response = (
                {
                    "product": RunnableLambda(itemgetter("product")).with_config(
                        run_name="Itemgetter:product"
                    ),
                    "user": RunnableLambda(itemgetter("user")).with_config(
                        run_name="Itemgetter:user"
                    )
                }
                | retrieve_chain
                | chain
        ).invoke({
            "product": product
        })
        print(response)


if __name__ == '__main__':
    main()
