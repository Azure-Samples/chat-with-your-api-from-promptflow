from azure.cosmos import exceptions
from azure.cosmos.aio import CosmosClient
import os

class cosmos_db_service:
    def __init__(self):
        endpoint = os.getenv('COSMOS_ENDPOINT')
        # Key should be stored in Key Vault with a Key Vault reference
        key = os.getenv('COSMOS_KEY')
        database_name = os.getenv('DATABASE_NAME')
        container_name = os.getenv('CONTAINER_NAME')

        if not all([endpoint, key, database_name, container_name]):
            raise ValueError("All configuration parameters must be provided and non-empty.")

        self.client = CosmosClient(endpoint, credential=key)
        try:
            database = self.client.get_database_client(database_name)
            self.container = database.get_container_client(container_name)
        except exceptions.CosmosResourceNotFoundError:
            raise ValueError("Database or Container does not exist.")

    async def close(self):
        await self.client.close()

    async def insert_session_async(self, session):
        created_item = await self.container.upsert_item(body=session)
        return created_item

    async def insert_message_async(self, message):
        created_item = await self.container.upsert_item(body=message)
        return created_item

    async def get_sessions_async(self):
        sessions = []
        query = "SELECT DISTINCT * FROM c WHERE c.type = 'Session'"
        items = self.container.query_items(query)
        async for item in items:
            sessions.append(item)
        return sessions

    async def get_session_messages_async(self, session_id):
        messages = []
        query = "SELECT * FROM c WHERE c.sessionId = @sessionId AND c.type = 'Message'"
        params = {'@sessionId': session_id}
        items = self.container.query_items(query, parameters=params)
        async for item in items:
            messages.append(item)
        return messages