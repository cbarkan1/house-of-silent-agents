from ollama import chat as ochat

def create_chat(model):
    def chat(message_record):
        return ochat(model, messages=message_record)["message"]["content"]
    return chat