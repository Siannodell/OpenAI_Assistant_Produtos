from utils import AssistantManager
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    manager = AssistantManager(api_key)

    manager.create_file("Arquivo-Análise-de-Pedidos-Saudável-to-Be.csv")

    manager.create_assistant(
        name="Assistente de análise de dados",
        instructions="Você é um assistente pessoal de análise de dados",
        tools=[{"type:" "retrieval"}]
    )

    manager.create_thread()

    manager.add_messages_to_thread(role="usuário", content="Qual é o mês com maior numero de pedidos?")
    manager.run_assistant(instructions="Qual é o mês com maior numero de pedidos?")
    manager.wait_for_completion()

if __name__ == "__main__":
    main()