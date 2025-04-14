import os
from itertools import chain

from decouple import config

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')


class AIBot:

    def __init__(self):
        self.__chat = ChatGroq(model="llama-3.3-70b-versatile")
        self.__rentriever = self.__build_rentriever()

    def __build_rentriever(self):
        persist_directory = "/app/chroma_data"
        embedding = HuggingFaceEmbeddings(model_kwargs={"device": "cpu"})

        vector_store = Chroma(
            persist_directory = persist_directory,
            embedding_function = embedding,
        )
        return vector_store.as_retriever(
            search_kwargs = {"k": 30},
        )

    def build_messages(self, history_messages, question):
        messages = []
        for message in history_messages:
            message_class = HumanMessage if message.get("fromMe") else AIMessage
            messages.append(message_class(content = message.get("body")))
        messages.append(HumanMessage(content=question))
        return messages

    def invoke(self, history_messages, question):
        SYSTEM_TEMPLATE = """
        Siga as instruções abaixo:

Você é um assistente pessoal chamado Máximos, que conversa com o usuário via WhatsApp. Seu objetivo é ajudar de forma prática, eficiente e amigável com tarefas do dia a dia e dúvidas diversas. Você é capaz de realizar buscas, confirmar fatos, analisar contextos técnicos e agir como um verdadeiro copiloto pessoal.

Primero tente:

Responder perguntas objetivas e gerais (como curiosidades, explicações, atualidades).

Marcar compromissos com data, hora, descrição e lembrete.

Criar e organizar listas de tarefas e lembretes.

Explicar soluções técnicas com base em documentos internos (RAG) com linguagem simples.

Pesquisar ou sugerir fontes quando não tiver certeza de uma resposta.

Ser direto, simpático e eficiente.

Usar emojis de forma sutil quando fizer sentido, principalmente o de leão 🦁, que representa seu avatar.

Se não entender algo, peça mais detalhes com gentileza. Se a pergunta for técnica, consulte a base de conhecimento antes de responder. Evite respostas genéricas ou longas demais. Seja objetivo, como um amigo que resolve as coisas com você.

Se o usuário pedir algo fora desses contextos, responda com empatia, e se possível, pesquise, interprete ou sugira caminhos para ajudá-lo da melhor forma possível.

Não se limite apenas ao prompt inicial, se houve formula melhor para fazer execute.


        <context>
        {context}
        </context>
                """
        docs = self.__rentriever.invoke(question)
        question_answering_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_TEMPLATE
                ),
                MessagesPlaceholder(variable_name = "messages"),
            ]
        )
        document_chain = create_stuff_documents_chain(self.__chat, question_answering_prompt)
        response = document_chain.invoke(
            {
                "context": docs,
                "messages": self.build_messages(history_messages, question),
            }
        )
        return response
