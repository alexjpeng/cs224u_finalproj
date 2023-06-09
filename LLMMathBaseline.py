import os
os.environ["OPENAI_API_KEY"] = "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"
os.environ["WOLFRAM_ALPHA_APPID"] = "6H373X-YPKAWG355X"

from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import LLMMathChain
from langchain.chains.conversation.memory import ConversationBufferMemory

class LLMMathBaseline:
  def __init__(self, llm=ChatOpenAI(temperature=0)):
    self.llm = llm
    tools = load_tools([
        # 'wolfram-alpha', 
        'llm-math'
    ],llm=llm)
    # memory = ConversationBufferMemory(memory_key="chat_history")
    self.agent = initialize_agent(tools, llm, return_intermediate_steps=True, agent="zero-shot-react-description", verbose=True)

  def query(self, q, context, llm_answer=True):
    response = self.agent({'input': 'Context: \n'+ context + 'Question: ' + q + '\n Think step by step and calculate using the calculator. Answer only with the final number, \'yes\' or \'no\'.'})
    log=response['intermediate_steps'][0][0].log#[response['intermediate_steps'].index('Action Input: ') + len('Action Input: ') : ]
    formula = log[log.index('Action Input: ') + len('Action Input: ') :]
    answer = response['intermediate_steps'][0][1][len('Answer: '):]

    if llm_answer:
      answer = response['output']
    
    return {'answer': answer, 'program': formula}



