from ollama import chat as ochat

def create_generate(model):
    def generate(message_record):
        return ochat(model, messages=message_record)["message"]["content"]
    return generate