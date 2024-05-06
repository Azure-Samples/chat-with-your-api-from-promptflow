import datetime
import uuid
from promptflow import tool
from datetime import date
from cosmos_db_service import cosmos_db_service
import os

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
async def process_input(question: str,chat_history: list, latitude: float, longitude: float, timezone: int, chatid: str) -> dict:
    # this node allows us to validate parameters passed from the front-end
    # e.g. a user location and local timezone
     # calculate today's date in YYY-MM-DD format and day
    
    # for our purposes server time is sufficient
    today = date.today()
    today_date = today.strftime("%Y-%m-%d")
    today_day = today.strftime("%A")

    chat_history = chat_history if chat_history else []

    # check if cosmos db is enabled
    is_cosmos_enabled = os.getenv('ENABLE_COSMOS_DB', 'false').lower() == 'true'

    if is_cosmos_enabled:
        session = {
            'id': str(uuid.uuid4()),
            'type': 'Session',
            'sessionId': chatid,
            'timeStamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        # set the message
        message = {
            'id': str(uuid.uuid4()),
            'type': 'Message',
            'sender': 'User',
            'sessionId': chatid,
            'timeStamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'text': str(question)
        }

        cosmos_service = cosmos_db_service()

        try:
            session_result = await cosmos_service.insert_session_async(session)
            message_result = await cosmos_service.insert_message_async(message)
        finally:
            await cosmos_service.close()

    question = question if question else "what is the weather at my current location?"
    # check for 0 latitude
    latitude = latitude if latitude else 37.7
    # check for 0 longitude
    longitude = longitude if longitude else -122.4

    # build a dict of all inputs and defaults to return    
    return {"question": question, "chatid": chatid, "chat_history": chat_history, "latitude":latitude, "longitude":longitude, "today_date": today_date, "today_day": today_day, "suggestions": ""}