## LangChain SQL Agent for dynamic data visualization 

Example application for the construction and inference of an LLM-based LangChain SQL Agent that can dynamically query a database and invoke multiple visualization tools.
The language model used is OpenAIs [GPT-4o mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/).

For this, four datasets from the [European Statistical Office](https://ec.europa.eu/eurostat/databrowser/explore/all/all_themes) (Eurostat) are loaded into a local SQL database that the LLM can query for up to 15 iterations per run. It can then use the results to independently call and output one of three basic visualizations functions based on Plotly.

The four datasets are all sourced from the _Health determinants_ part of Eurostats public dataset API and include statistics on:
- **tobacco consumption** by country of citizenship for the years 2014 and 2019 ([Link](https://ec.europa.eu/eurostat/databrowser/view/hlth_ehis_sk1c/default/table?lang=en))
- **body mass index** (BMI) by country of citizenship for the years 2014 and 2019 ([Link](https://ec.europa.eu/eurostat/databrowser/view/hlth_ehis_bm1c/default/table?lang=en))
- **physical exercise** by country of citizenship for the years 2014 and 2019 ([Link](https://ec.europa.eu/eurostat/databrowser/view/hlth_ehis_pe9c/default/table?lang=en))
- **alcohol consumption** by country of citizenship for the years 2014 and 2019 ([Link](https://ec.europa.eu/eurostat/databrowser/view/hlth_ehis_al1c/default/table?lang=en))

The LLM agent can use the following three tool functions to visualize the results (see [agent_tools.py](https://github.com/EliasK93/LangChain-SQL-Agent-for-dynamic-data-visualization/blob/master/agent_tools.py)):
- **output_table()**: output 2D table contents as a pretty table using Plotly table viewer
- **output_bar_plot()**: output a simple bar plot
- **output_time_series_plot()**: output one or multiple line plots along one main time axis

<br>


### Example Results

<table>
    <thead>
        <tr>
            <th>Input</th>
            <th>Main SQL query used by the LLM</th>
            <th colspan="2">Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Show me the change in the percentage points of daily smokers between 2014 and 2019 for Germany, Denmark, Poland and Austria in a pretty table (one row per country).</td>
            <td><pre><code>SELECT "country (ISO-639-1)", "daily smoker"</code><br><code>FROM smoking_of_tobacco_products</code><br><code>WHERE year IN ('2014', '2019')</code><br><code>AND "country (ISO-639-1)" IN ('DE', 'DK', 'PL', 'AT');</code></pre></td>
            <td>Here is the change in the percentage points of daily smokers between 2014 and 2019 for Germany, Denmark, Poland, and Austria:<br><br>| Country  | 2014 Daily Smokers (%) | 2019 Daily Smokers (%) | Change in Percentage Points |<br>|----------|------------------------|------------------------|-----------------------------|<br>| Austria  | 22.4                   | 19.1                   | -3.3                        |<br>| Germany  | 15.7                   | 22.5                   | 6.8                         |<br>| Denmark  | 13.8                   | 12.7                   | -1.1                        |<br>| Poland   | 22.7                   | 19.4                   | -3.3                        |</td>            
            <td><img src="imgs/result-query1.png" alt="imgs/result-query1.png" /></td>
        </tr>
        <tr>
            <td>Plot the percentage of people who are obese in Germany, Denmark, Estonia, Finland, Poland and Austria as a time series (one series per country).</td>
            <td><pre><code>SELECT year, "country (ISO-639-1)", obese</code><br><code>FROM body_mass_index</code><br><code>WHERE "country (ISO-639-1)" IN ('DE', 'DK', 'EE', 'FI', 'PL', 'AT')</code><br><code>ORDER BY year;</code></pre></td>
            <td>I have plotted the percentage of obese people in Germany, Denmark, Estonia, Finland, Poland, and Austria for the years 2014 and 2019. The data shows the following obesity rates:<br><br>- **Austria (AT)**: 48.0% (2014), 51.4% (2019)<br>- **Germany (DE)**: 50.8% (2014), 52.4% (2019)<br>- **Denmark (DK)**: 46.2% (2014), 49.3% (2019)<br>- **Estonia (EE)**: 51.4% (2014), 53.6% (2019)<br>- **Finland (FI)**: 53.7% (2014), 58.3% (2019)<br>- **Poland (PL)**: 53.3% (2014), 56.8% (2019)<br><br>If you need further analysis or a different visualization, let me know!</td>
            <td><img src="imgs/result-query2.png" alt="imgs/result-query2.png" /></td>
        </tr>
        <tr>
            <td>Calculate the minimum, average and maximum percentages of people in 2019 who do only aerobic, only muscle-strengthening and both aerobic and muscle-strengthening exercise and show the result as a bar plot (nine bars overall).</td>
            <td><pre><code>SELECT</code><br><code>    MIN(aerobic) AS min_aerobic,</code><br><code>    AVG(aerobic) AS avg_aerobic,</code><br><code>    MAX(aerobic) AS max_aerobic,</code><br><code>    MIN("muscle-strengthening") AS min_muscle_strengthening,</code><br><code>    AVG("muscle-strengthening") AS avg_muscle_strengthening,</code><br><code>    MAX("muscle-strengthening") AS max_muscle_strengthening,</code><br><code>    MIN("aerobic and muscle-strengthening") AS min_aerobic_and_strengthening,</code><br><code>    AVG("aerobic and muscle-strengthening") AS avg_aerobic_and_strengthening,</code><br><code>    MAX("aerobic and muscle-strengthening") AS max_aerobic_and_strengthening</code><br><code>FROM health_enhancing_physical_activity</code><br><code>WHERE year = '2019';</code></pre></td>
            <td>I have calculated the minimum, average, and maximum percentages of people in 2019 who do only aerobic, only muscle-strengthening, and both aerobic and muscle-strengthening exercises. Here are the results:<br><br>- **Aerobic Exercise:**<br>  - Minimum: 7.9%<br>  - Average: 29.90%<br>  - Maximum: 61.5%<br><br>- **Muscle-Strengthening Exercise:**<br>  - Minimum: 2.0%<br>  - Average: 20.43%<br>  - Maximum: 43.9%<br><br>- **Both Aerobic and Muscle-Strengthening Exercise:**<br>  - Minimum: 1.7%<br>  - Average: 13.27%<br>  - Maximum: 32.6%<br><br>Unfortunately, I encountered an issue while trying to generate the bar plot. However, you can visualize the data using the above statistics. If you need further assistance or a different format, please let me know!</td>
            <td><img src="imgs/result-query3.png" alt="imgs/result-query3.png" /></td>
        </tr>
        <tr>
            <td>What are the five countries with most people who in 2014 stated that they have not drunk alcohol in the last year? Plot the result as a bar plot.</td>
            <td><pre><code>SELECT "country (ISO-639-1)", "never or not in the last 12 months"</code><br><code>FROM alcohol_consumption</code><br><code>WHERE year = '2014'</code><br><code>ORDER BY "never or not in the last 12 months" DESC</code><br><code>LIMIT 5;</code></pre></td>
            <td>The five countries with the most people who stated they have not drunk alcohol in the last year in 2014 are:<br><br>1. Turkey (TR) - 85.1%<br>2. Cyprus (CY) - 45.4%<br>3. Croatia (HR) - 43.8%<br>4. Romania (RO) - 42.1%<br>5. Bulgaria (BG) - 34.0%<br><br>I have plotted the results as a bar plot.</td>
            <td><img src="imgs/result-query4.png" alt="imgs/result-query4.png" /></td>
        </tr>
    </tbody>
</table>
<br>

### Requirements

##### - Python >= 3.10

##### - pip
  - `langchain`
  - `langchain-community`
  - `langchain-openai`
  - `sqlalchemy`
  - `pydantic`
  - `pandas`
  - `plotly`
