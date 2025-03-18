import os
from langchain_groq import ChatGroq  
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv

# Set API Key
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama3-70b-8192", temperature=0.7, api_key=api_key)

def generate_restaurant_name_and_items(cuisine):
  
    prompt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for it."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    prompt_template_menu = PromptTemplate(
        input_variables=["restaurant_name"],
        template="Suggest some menu items for {restaurant_name} restaurant. "
                 "Format them as a numbered list like:\n1. Dish Name\n2. Dish Name\n3. Dish Name"
    )
    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_menu, output_key="menu_items")

   
    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']
    )

    response = chain({'cuisine': cuisine})

    
    print("RAW RESPONSE:", response)

  
    if not isinstance(response, dict):
        return {"restaurant_name": "Unknown", "menu_items": []}


    restaurant_name = response.get("restaurant_name", "").strip()

  
    menu_items_raw = response.get("menu_items", "").strip()
    menu_items_list = [item.split(". ", 1)[-1].strip() for item in menu_items_raw.split("\n") if item.strip()]

    return {
        "restaurant_name": restaurant_name,
        "menu_items": menu_items_list
    }


if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Indian"))
