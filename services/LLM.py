import redis
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .vector_db import vector_store
import os

HOST = os.getenv("HOST")
PASSWORD = os.getenv("PASSWORD")
GROQ_KEY = os.getenv("GROQ_KEY")



# Initialize Redis
redis_client = redis.Redis(
    host=HOST,
    port=13489,
    decode_responses=True,
    username="default",
    password=PASSWORD,
)

# Initialize LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=1,
    groq_api_key=GROQ_KEY
)

def get_chat_response(user_id, user_message):
    history_key = f"chat_history:{user_id}"
    
    docs = vector_store.similarity_search(user_message, k=3, filter={"user_id": user_id})
    context = "\n".join([d.page_content for d in docs])

    raw_history = redis_client.lrange(history_key, 0, 19)
    formatted_history = "\n".join(reversed(raw_history))

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant. 
        Use the provided context to answer the user's question.
        If the answer isn't in the context, Say i dont know.
        
        CONTEXT: {context}
        HISTORY: {old_chat}"""),
        ("user", "{message}")
    ])

    chain = prompt | llm | StrOutputParser()
    
    
    response = chain.invoke({
        "message": user_message, 
        "old_chat": formatted_history,
        "context": context
    })


    redis_client.lpush(history_key, f"User: {user_message} | AI: {response}")
    redis_client.ltrim(history_key, 0, 19)
    return response