from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
import templates as t


class Chat:
    conversation: None

    def __init__(self):
        llm = ChatOpenAI(temperature=0.7)
        memory = ConversationBufferMemory(return_messages=True)
        system_message = """
あなたはずんだもんです。一つずつユーザーと対話しながら日記を書くエージェントです。
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_message),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        self.conversation = ConversationChain(
            memory=memory,
            llm=llm,
            prompt=prompt
        )

    def start(self):
        return self.conversation.predict(input=t.chat_template().format())

    def reply(self, message):
        return self.conversation.predict(input=message)
