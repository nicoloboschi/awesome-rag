# awesome-rag

# RAG phases
- Loading
- Splitting
- Storage
- Retrieval
- Generation



## Loading
### Clean data
Are the topics broken out logically? Are topics covered in one place or many separate places? If you, as a human, can’t easily tell which document you would need to look at to answer common queries, your retrieval system won’t be able to either.
Use the LLM to create summaries of all the documents provided as context. The retrieval step can then first run a search over these summaries, and dive into the details only when necessary

## Splitting
### Chunk size
Frameworks abstract away the chunking process and allow you to get away without thinking about it. But you should think about it. Chunk size matters.
https://www.pinecone.io/learn/chunking-strategies/

## Storage
### Hybrid search
You may want to explore key-word based search. It doesn’t have to be one or the other, many applications use a hybrid. For example, you may use a key-word based index for queries relating to a specific product, but rely on embeddings for general customer support.


## Retrieval 
- Re ranking
- MuRAG  Multimodal Retrieval-Augmented Transforme - Rag for Images  - https://arxiv.org/abs/2210.02928
- REALM - Retrieval-Augmented Language Model -  https://arxiv.org/abs/2002.08909


# Resources
- https://towardsdatascience.com/10-ways-to-improve-the-performance-of-retrieval-augmented-generation-systems-5fa2cee7cd5c
