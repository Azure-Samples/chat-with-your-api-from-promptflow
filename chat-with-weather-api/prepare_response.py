
import datetime
import os
import uuid
from promptflow import tool
import json

from cosmos_db_service import cosmos_db_service


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
async def prepare_response(user_intent: str, api_response: dict, analyze_api_response: str, chatid: str) -> dict:
    
     # check if cosmos db is enabled
    is_cosmos_enabled = os.getenv('ENABLE_COSMOS_DB', 'false').lower() == 'true'
    
    if is_cosmos_enabled:
        message = {
            'id': str(uuid.uuid4()),
            'type': 'Message',
            'sender': 'Assistant',
            'sessionId': chatid,
            'timeStamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'chatResponse': json.dumps(analyze_api_response),
            'apiResponse': json.dumps(api_response),
        }
        
        cosmos_service = cosmos_db_service()

        try:
            message_result = await cosmos_service.insert_message_async(message)
        finally:
            await cosmos_service.close()

    return {"chat_response": analyze_api_response, "api_response": api_response}
