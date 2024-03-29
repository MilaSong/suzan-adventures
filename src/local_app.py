from elasticsearch import Elasticsearch
import os
from langchain.memory import ElasticsearchChatMessageHistory, ConversationBufferMemory
from langchain_openai import OpenAI
from langchain.chains.llm import LLMChain
from langchain_core.prompts.prompt import PromptTemplate 
from dotenv import load_dotenv
load_dotenv()

# Password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")

# Create the client instance
client = Elasticsearch(
    hosts=["https://localhost:9200"],
    verify_certs=False, # TODO: Add links to certs
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

message_history = ElasticsearchChatMessageHistory(
    es_connection=client,
    index="test-history", 
    session_id="test-session"
)

message_history.clear()

elastic_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
)

template = """
You are now the AI guide of a mystical journey in the Whispering Woods. 
A Human traveler named Elara seeks the lost Gem of Serenity. 
You must navigate her through challenges, choices, and consequences, 
dynamically adapting the tale based on the traveler's decisions. 
Your goal is to create a branching narrative experience where each choice 
leads to a new path, ultimately determining Elara's fate. 

Here are some rules to follow:
1. Start by asking the Human player to choose some kind of weapons that will be used later in the game
2. Have a few paths that lead to success
3. Have some paths that lead to death. If the user dies generate a response that explains the death and ends in the text: "The End.", I will search for this text to end the game
4. Do not answer the questions yourself. The answers must be given by the player

Here is the chat history, use this to understand what to say next: {chat_history}
You must only answer the AI part and wait for human input.
Human: {human_input}
AI:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=template
)

llm = OpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"), model_kwargs={"stop": ["Human:", "AI:"]})
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=elastic_buff_memory
)

choice = "start"
while True:
    response = llm_chain.predict(human_input=choice)
    print(response.strip())

    if "The End." in response:
        break

    choice = input("Your reply: ")
