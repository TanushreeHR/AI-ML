import openai
import langchain
from langchain.llms import OpenAI

# print('ChatOpenAI available')
llm = OpenAI(
    temperature = 0.3,
    api_key="7639e32bb29f49debd96bff0d886937c"
)
response = llm("Explain LangChain in simple terms.")
print(response)