import json
import pandas as pd
import plotly.graph_objects as go
from langchain.agents import tool
from plotly.express.colors import qualitative as colors


@tool
def output_table(data: str) -> None:
    """
    Outputs a pretty table using plotly.
    data has to be a dictionary-formatted string with column names as keys and column values as values.

    Example input:
    data = '{"year": [2019, 2020, 2021], "price": [43.30, 53.40, 34.10]}'
    """
    if type(data) == dict:
        data = json.dumps(data)
    data = json.loads(data)
    df = pd.DataFrame(data)
    fig = go.Figure(data=[go.Table(header={'values': list(df.columns), 'fill_color': colors.Set2[5], 'align': 'left'},
                    cells={'values': [df[col] for col in df.columns], 'fill_color': colors.Pastel2[5], 'align': 'left'})])
    fig.show()


@tool
def output_bar_plot(data: str, title: str) -> None:
    """
    Outputs a bar plot using plotly.
    data has to be a dictionary-formatted string with exactly two key-value pairs.
    Uses the first key-value pair as the x-axis and the second as the y-axis.

    Example input:
    data = '{"year": [2019, 2020, 2021], "price": [43.30, 53.40, 34.10]}'
    title = 'Prices and Sales between 2019 and 2021'
    """
    if type(data) == dict:
        data = json.dumps(data)
    data = json.loads(data)
    fig = go.Figure()
    x, y = data.keys()
    for x_value, y_value in zip(data[x], data[y]):
        fig.add_trace(go.Bar(x=[x_value], y=[y_value], name=str(x_value)))
    fig.update_layout(xaxis_title=x, yaxis_title=y, title=title)
    fig.show()


@tool
def output_time_series_plot(data: str, title: str) -> None:
    """
    Outputs a time series plot using plotly.
    data has to be a dictionary-formatted string with two or more key-value pairs.
    Uses the first key-value pair as the x-axis, and other key-value pairs as the different y-axes.

    Example input:
    data = '{"year": [2019, 2020, 2021], "price": [43.30, 53.40, 34.10], "sales": [100, 150, 200]}'
    title = 'Prices and Sales between 2019 and 2021'
    """
    if type(data) == dict:
        data = json.dumps(data)
    data = json.loads(data)
    fig = go.Figure()
    x_axis = list(data.keys())[0]
    x_vals = data[x_axis]
    for y_axis in list(data.keys())[1:]:
        fig.add_trace(go.Scatter(x=x_vals, y=data[y_axis], mode='markers+lines', name=y_axis))
    fig.update_layout(xaxis_title=x_axis, yaxis_title="Values", title=title, xaxis={"tickmode": "array", "tickvals": x_vals})
    fig.show()
