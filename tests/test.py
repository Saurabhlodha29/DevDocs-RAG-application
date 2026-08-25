from langchain_groq import ChatGroq


from dotenv import load_dotenv


load_dotenv()

model = ChatGroq(model = "openai/gpt-oss-20b")

result = model.invoke('hi')
print(result)