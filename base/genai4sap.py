from dataclasses import dataclass
from typing import List, Optional, Dict, Union, Literal
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import requests
from utilities import (BACKEND_URL, ADMIN_API_KEY, CHAT_API)


@dataclass
class BaseResponse:
    agent_id: str
    agent_name: str
    type: str

@dataclass
class TextResponse(BaseResponse):
    type: Literal["text"]
    text: str
    id: Optional[str] = None

@dataclass
class SQLResponse(BaseResponse):
    type: Literal["sql"]
    text: str
    id: Optional[str] = None

@dataclass
class DataFrameResponse(BaseResponse):
    type: Literal["df"]
    df: pd.DataFrame
    id: Optional[str] = None

@dataclass
class PlotlyResponse(BaseResponse):
    type: Literal["plotly_figure"]
    fig: go.Figure
    id: Optional[str] = None

@dataclass
class ChatResponse:
    text_responses: List[TextResponse]
    sql_responses: List[SQLResponse]
    df_responses: List[DataFrameResponse]
    plotly_responses: List[PlotlyResponse]

def call_chat_api(user_question) -> ChatResponse:
    endpoint = f"{BACKEND_URL}{CHAT_API}"
    headers = {"ADMIN-API-KEY": ADMIN_API_KEY, "Content-Type": "application/json"}
    body = {"message": user_question}
    
    text_responses: List[TextResponse] = []
    sql_responses: List[SQLResponse] = []
    df_responses: List[DataFrameResponse] = []
    plotly_responses: List[PlotlyResponse] = []

    try:
        response = requests.post(endpoint, headers=headers, json=body)
        response.raise_for_status()
        
        for line in response.text.split('\n'):
            if line.strip() and line.startswith('data: '):
                try:
                    data = json.loads(line[6:])  # Skip 'data: ' prefix
                    
                    if data['type'] == 'text':
                        text_responses.append(TextResponse(**data))
                    elif data['type'] == 'sql':
                        sql_responses.append(SQLResponse(**data))
                    elif data['type'] == 'df':
                        # Convert the df string to actual DataFrame
                        df_data = json.loads(data['df'])
                        data['df'] = pd.DataFrame(df_data)
                        df_responses.append(DataFrameResponse(**data))
                    elif data['type'] == 'plotly_figure':
                        # Convert the fig string to Plotly figure
                        fig_data = json.loads(data['fig'])
                        data['fig'] = go.Figure(fig_data)
                        plotly_responses.append(PlotlyResponse(**data))
                        
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    continue
        
        return ChatResponse(
            text_responses=text_responses,
            sql_responses=sql_responses,
            df_responses=df_responses,
            plotly_responses=plotly_responses
        )
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling chat API: {e}")
