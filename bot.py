# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import (
    Activity,
    ChannelAccount,
    Attachment)
from botframework.connector import ConnectorClient
from botframework.connector.auth import MicrosoftAppCredentials
from base.genai4sap import call_chat_api, ChatResponse
import requests
import pandas as pd
import json

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        user_question = turn_context.activity.text
        try:
            await turn_context.send_activity(f"¡Gran pregunta! Déjame cumplir tu petición...")

            response: ChatResponse = call_chat_api(user_question)

            if response:  # Check if response is not None (meaning no errors occurred)
                for text_resp in response.text_responses:
                    await turn_context.send_activity(f"**{text_resp.agent_name}:**")
                    await turn_context.send_activity(f"{text_resp.text}")
                # Process SQL responses
                for sql_resp in response.sql_responses:
                    await turn_context.send_activity(f"**{sql_resp.agent_name}**:")
                    await turn_context.send_activity(f"Aquí está el SQL que generé:\n\n ``{sql_resp.text}``")
                # Process DataFrame responses
                for df_resp in response.df_responses:
                    df_markdown = df_resp.df.to_markdown(index=False)
                    await turn_context.send_activity(f"**{df_resp.agent_name}:**")
                    await turn_context.send_activity(f"Y aquí están los resultados:\n```\n{df_markdown}\n```")
             
            else: # If the response is None (error in chat_api call), send a user-friendly message
                await turn_context.send_activity(f"Lo siento, encontré un error al procesar su solicitud. Inténtelo de nuevo más tarde.")

        except Exception as e:
            # Handle exceptions with a user-friendly message
            await turn_context.send_activity(f"Lo siento, encontré un error al procesar su solicitud. Inténtelo de nuevo más tarde.")
            print(f"Error processing request: {e}")  # Log the error for debugging

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("¡Hola!, soy el asistente de GenAI4SAP, ¿en qué puedo ayudarte hoy?")
