
from promptflow import tool
import json


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def prepare_response(user_intent: str, api_response: dict, analyze_api_response: str) -> dict:
    
    return {"chat_response": analyze_api_response, "api_response": api_response}
