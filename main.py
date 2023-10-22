from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
import json
import os

pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")

def docs_to_text_retriever(retriever, custom_instruction=None):
    def _retriever(query):
        docs = retriever(query)
        text = custom_instruction or ""
        for d in docs:
            text += f"{d.page_content.strip()}\n\n"

        return text

    return _retriever

_retriever = Pinecone.from_existing_index(index_name="agentmatscience", embedding=OpenAIEmbeddings()).as_retriever(search_kwargs = {"k": 10})

retriever = docs_to_text_retriever(retriever=_retriever.get_relevant_documents)

app = Flask(__name__)
CORS(app)

def ask(query):

    response = retriever(query)

    prompt = [
        SystemMessage(content="You will take user instruction and relevant content, and you should answer the user instruction using the content, the answer will be added to a note taking app.\n"
                                "Never answer in first person. The answer will be added to a note taking app.\n"
                                "Answer in a format that is easy, short, and to the point, to be added to a note taking app.\n"),
        HumanMessagePromptTemplate.from_template(
            "User question: {user_question}\n\n"
            "Relevant content:\n"
            "{relevant_content}\n\n"
            "Answer: "
        ),
    ]

    chat_prompt_template = ChatPromptTemplate.from_messages(prompt)

    llm_chat = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k-0613")

    answer = llm_chat(chat_prompt_template.format_messages(user_question=query, relevant_content=response)).content

    return answer