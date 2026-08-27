from vector_store import vector_store

# Define a function that performs the retrieval given a user query

def retrieve(user_query:str) -> list:
    retriever = vector_store.as_retriever(search_kwargs = {'k':4})

    results = retriever.invoke(user_query)
    
    context = []
    
    for i,doc in enumerate(results):
        context.append(doc.page_content)
        
    return context