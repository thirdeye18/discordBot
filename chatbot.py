from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


"""
Chatbot client
Author: Justin Hammel
Description: Script instantiates chatbot using chatterbot and training with corpus database in the trainer.py file.
"""

chatbot = ChatBot('2d')

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    "chatterbot.corpus.english"
)

response = chatbot.get_response("Good morning!")

print(response)
