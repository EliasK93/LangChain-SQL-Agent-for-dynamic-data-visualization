# eurostat settings
base_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/hlth_ehis_"
country_query_string = "BE+BG+CZ+DK+DE+EE+IE+EL+ES+FR+HR+IT+CY+LV+LT+LU+HU+MT+NL+AT+PL+PT+RO+SI+SK+FI+SE+IS+NO+UK+TR"
format_query_string = "/?format=TSV"
datasets = {
    "smoking_of_tobacco_products": {
        "url": base_url + "sk1c/A.PC.NSM+SM_DAY+SM_OCC.T.TOTAL.NAT." + country_query_string + format_query_string,
        "category_map": {"NSM": "non-smoker", "SM_DAY": "daily smoker", "SM_OCC": "occasional smoker"}},
    "body_mass_index": {
        "url": base_url + "bm1c/A.PC.BMI_LT18P5+BMI18P5-24+BMI_GE25.T.TOTAL.NAT." + country_query_string + format_query_string,
        "category_map": {"BMI_LT18P5": "underweight", "BMI18P5-24": "normal weight", "BMI_GE25": "obese"}},
    "health_enhancing_physical_activity": {
        "url": base_url + "pe9c/A.PC.MV_AERO_MSC+MV_AERO+MV_MSC.T.TOTAL.NAT." + country_query_string + format_query_string,
        "category_map": {"MV_AERO_MSC": "aerobic and muscle-strengthening", "MV_AERO": "aerobic", "MV_MSC": "muscle-strengthening"}},
    "alcohol_consumption": {
        "url": base_url + "al1c/A.PC.DAY+WEEK+MTH+LT1M+NVR_NM12.T.TOTAL.NAT." + country_query_string + format_query_string,
        "category_map": {"DAY": "every day", "WEEK": "every week", "MTH": "every month", "LT1M": "less than once a month", "NVR_NM12": "never or not in the last 12 months"}},
}

# local database settings
database_url = "sqlite:///sql_database.db"

# llm settings
openai_key = "..."  # omitted in version control
llm_model_id = "gpt-4o-mini"
llm_temperature = 0.1

# agent settings
agent_max_iterations = 15
agent_max_execution_time = 30
