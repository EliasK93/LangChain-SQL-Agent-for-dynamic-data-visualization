import re
import os
import numpy as np
import pandas as pd
from langchain.agents import AgentExecutor
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from sqlalchemy import create_engine
import agent_tools
from config import openai_key, llm_model_id, llm_temperature, agent_max_execution_time, agent_max_iterations, \
    database_url, datasets


def load_and_clean_eurostat_df(dataset: dict[str: str | dict]) -> pd.DataFrame:
    """
    Load the datasets from their eurostat URLs as pandas DataFrames, clean them and format them in a format easy to
    understand for the LLM. The formatted DataFrames have one row per country and year and one column for each unique
    category, for example:

        country (ISO-639-1) year    daily smoker    non-smoker  occasional smoker
        ...                 ...     ...             ...         ...
        IS                  2014    11,2            81,9        6,9
        IS                  2019    NaN             NaN         NaN
        IT                  2014    17,6            77,5        4,9
        IT                  2019    17,3            77,6        5,1
        ...                 ...     ...             ...         ...
    """

    # load TSV file from URL
    df = pd.read_csv(dataset["url"], sep="\t")
    # split index column at commas, then select only the category name, country name and 2014 and 2019 values
    df = pd.concat([df[df.columns[0]].str.split(',', expand=True), df[df.columns[1:]]], axis=1).iloc[:, [2, 6, 7, 8]]
    # set clean column names
    df.columns = ["category", "country (ISO-639-1)", "2014", "2019"]
    # map category codes to readable category labels
    df["category"] = df["category"].map(dataset["category_map"])
    # for all numeric cells: strip, clean trailing text from numbers and set all non-parsables to np.nan
    for col in ["2014", "2019"]:
        df[col] = df[col].apply(lambda val: (m := re.match(r"-?\d*\.?\d+", str(val).strip())) and float(m.group(0)) or np.nan)
    # convert from wide to long w.r.t. year
    df = pd.melt(df, id_vars=["country (ISO-639-1)", "category"], var_name="year", value_name="value")
    # convert from long to wide w.r.t. to categories
    df = df.pivot(index=['country (ISO-639-1)', 'year'], columns='category', values='value').reset_index()

    return df


def load_sql_database() -> SQLDatabase:
    """
    Load the datasets from their eurostat URLs as pandas DataFrames, format them properly, then convert them to SQL and
    add them to a local SQLDatabase.
    """

    # setup SQLite database
    engine = create_engine(database_url)
    # load datasets and put them into database
    for dataset in datasets:
        load_and_clean_eurostat_df(datasets[dataset]).to_sql(dataset, engine, index=False, if_exists="replace")
    return SQLDatabase(engine=engine)


def load_llm() -> ChatOpenAI:
    """
    Load the OpenAI model using the key and model_id specified in config.
    """

    # set API key
    os.environ["OPENAI_API_KEY"] = openai_key
    # load OpenAI model
    return ChatOpenAI(model=llm_model_id, temperature=llm_temperature)


def load_sql_agent(db: SQLDatabase, llm: ChatOpenAI) -> AgentExecutor:
    """
    Create the Langchain SQL AgentExecutor using the settings specified in config, also hand the tool functions to
    the AgentExecutor.
    """
    # set extra tools the agent can use
    extra_tools = [agent_tools.output_bar_plot, agent_tools.output_time_series_plot, agent_tools.output_table]
    # create SQL agent
    return create_sql_agent(llm, db=db, agent_type="openai-tools", max_iterations=agent_max_iterations,
                            max_execution_time=agent_max_execution_time, extra_tools=extra_tools, verbose=True)


if __name__ == '__main__':

    # load SQLDatabase
    db = load_sql_database()

    # load OpenAI model
    llm = load_llm()

    # load SQL AgentExecutor
    sql_agent = load_sql_agent(db, llm)

    # hand some test queries to the agent
    for query in ["Show me the change in the percentage points of daily smokers between 2014 and 2019 for Germany, Denmark, Poland and Austria in a pretty table (one row per country).",
                  "Plot the percentage of people who are obese in Germany, Denmark, Estonia, Finland, Poland and Austria as a time series (one series per country).",
                  "Calculate the minimum, average and maximum percentages of people in 2019 who do only aerobic, only muscle-strengthening and both aerobic and muscle-strengthening exercise and show the result as a bar plot (nine bars overall).",
                  "What are the five countries with most people who in 2014 stated that they have not drunk alcohol in the last year? Plot the result as a bar plot."]:

        answer = sql_agent.invoke({"input": query})["output"]
        print(answer)
