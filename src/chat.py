from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import (
    HumanMessage,
)
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
import templates as t
from slack_message import SlackMessage


class Chat:
    conversation: None

    def __init__(self):
        llm = ChatOpenAI(temperature=0.5)
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

    def finish(self, last_message):
        llm = ChatOpenAI(temperature=0.5)
        result = llm([HumanMessage(
            content=t.diary_template().format(text=last_message))])
        slack_message = SlackMessage()
        slack_message.send(result.content)

    def reply(self, message):
        return self.conversation.predict(input=message)

    def is_finished(self, message):
        # FIXME
        return (
                ("さらばなのだ。また会おうなのだ。" in message) or
                ("今日の日記をまとめるのだ" in message) or
                ("よろしいでしょうか" in message) or
                ("以上の内容" in message) or
                ("以下の内容" in message)
        )
