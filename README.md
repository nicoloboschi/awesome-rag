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




## Retrieval 
- Re ranking
- MuRAG  Multimodal Retrieval-Augmented Transforme - Rag for Images  - https://arxiv.org/abs/2210.02928
- REALM - Retrieval-Augmented Language Model -  https://arxiv.org/abs/2002.08909
