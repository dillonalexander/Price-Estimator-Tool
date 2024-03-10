import streamlit as st
import datetime
import altair as alt
import requests
import snowflake.connector
import pandas as pd
import json
from dotenv import load_dotenv
import os
import base64
from pathlib import Path
import utils.helper as helper
import logging

load_dotenv()

ESTIMATE_MODEL_SECRET = os.getenv("ESTIMATE_MODEL_SECRET")
if ESTIMATE_MODEL_SECRET is None:
    raise ValueError("Environment variable 'ESTIMATE_MODEL_SECRET' not found.")

VEHICLE_RESOLVER_TOKEN_ENDPOINT = os.getenv("VEHICLE_RESOLVER_TOKEN_ENDPOINT")
if VEHICLE_RESOLVER_TOKEN_ENDPOINT is None:
    raise ValueError("Environment variable 'VEHICLE_RESOLVER_TOKEN_ENDPOINT' not found.")

PRICE_ESTIMATOR_CLIENT_SECRET = os.getenv("PRICE_ESTIMATOR_CLIENT_SECRET")
if PRICE_ESTIMATOR_CLIENT_SECRET is None:
    raise ValueError("Environment variable 'PRICE_ESTIMATOR_CLIENT_SECRET' not found.")

SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
if SNOWFLAKE_PASSWORD is None:
    raise ValueError("Environment variable 'SNOWFLAKE_PASSWORD' not found.")

SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
if SNOWFLAKE_DATABASE is None:
    raise ValueError("Environment variable 'SNOWFLAKE_DATABASE' not found.")


current_date  = datetime.date.today()
state_names = [
    "Alabama","Arizona","Arkansas","California","Colorado","Florida","Georgia",
    "Idaho","Illinois","Indiana","Iowa","Kentucky","Louisiana","Massachusetts",
    "Michigan","Minnesota","Missouri","Nevada","New Jersey","New York","North Carolina",
    "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","South Dakota","Tennessee",
    "Texas","Utah","Virginia","Washington",
]  # Only states with locations the valuation model uses

if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

if "timeframe_filter" not in st.session_state:
    st.session_state.timeframe_filter = "8 Weeks"

if "form_data" not in st.session_state:
    st.session_state["form_data"] = False

st.set_page_config(
    page_title="Price Estimator",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
def get_vehicle_resolver_token():
    response = helper.get_vehicle_resolver_token_data()
    if response["status_code"] == 200:
        return f"Bearer {response['access_token']}"
    else:
        print("Error", f"There was an issue with your request: {response}")
    # vehicle_resolver_token_endpoint = VEHICLE_RESOLVER_TOKEN_ENDPOINT
    # payload = {
    #     "client_id": "price-estimator",
    #     "client_secret": PRICE_ESTIMATOR_CLIENT_SECRET,
    # }
    # response = requests.post(vehicle_resolver_token_endpoint, data=payload, verify=False)
    # if response.status_code == 200:
    #     return f"Bearer {response.json()['access_token']}"
    # else:
    #     print("Error", f"There was an issue with your request: {response.json()}")
 


def get_vehicle_description(vin):
    response = helper.get_vehicle_description_data(vin)
    if response["status_code"] == 200:
        year = response["data"]["VINDescription"]["result"]["year"]
        make = response["data"]["VINDescription"]["result"]["make"]
        model = response["data"]["VINDescription"]["result"]["model"]
        trim = response["data"]["VINDescription"]["result"]["vehicles"][0]["trim"] or None  # If trim is not available, set to None
        return year, make, model, trim
    else:
        print("Error", f"There was an issue with your request: {response}")
    # get_vehicle_description_header_dict = {"Content-Type": "application/json", "Authorization": get_vehicle_resolver_token()}
    # vehicle_description_endpoint = VEHICLE_DESCRIPTION_ENDPOINT
    # vehicle_description_query = """
    # query {
    #     VINDescription(VIN: $vin) {
    #         message
    #         error
    #         result {
    #             vinProcessed
    #             validVin
    #             validationErrorMessage
    #             buildMSRP
    #             year
    #             make
    #             model
    #             vehicles {
    #                 styleDescription
    #                 trim
    #                 bodyType
    #             }
    #         }
    #     }
    # }
    # """
    # vehicle_variables = {"vin": vin}
    # vehicle_description_response = requests.post(vehicle_description_endpoint, json={"query": vehicle_description_query, "variables": vehicle_variables}, headers=get_vehicle_description_header_dict, verify=False)

    # if vehicle_description_response.status_code == 200:
    #     year = vehicle_description_response.json()["data"]["VINDescription"]["result"]["year"]
    #     make = vehicle_description_response.json()["data"]["VINDescription"]["result"]["make"]
    #     model = vehicle_description_response.json()["data"]["VINDescription"]["result"]["model"]
    #     trim = vehicle_description_response.json()["data"]["VINDescription"]["result"]["vehicles"][0]["trim"] or None  # If trim is not available, set to None
    #     return year, make, model, trim
    # else:
    #     print("Error", f"There was an issue with your request: {vehicle_description_response.json()}")


def estimate_model_api_call(vin, condition_grade, odometer_mi, state, trim=None, drivable_indicator="DRIVABLE", client_floor_price=None, client_name="test"):
    response = helper.get_estimate_model_api_call_data(vin)
    if response["results"][0]["result"]["results"][0]["price"] == None:
        raise ValueError("Estimate Model API returned a None value for price")
    
    prices_and_probabilities = [(
        result["result"]["results"][0]["price"],
        result["result"]["results"][0]["predicted_prob"],
        result["result"]["results"][0]["trim_match"],
        result["result"]["results"][0]["price_low"],
        result["result"]["results"][0]["price_high"],
        )
        for result in response["results"]
    ]
    model_data = (current_date.strftime("%Y-%m-%d"),) + prices_and_probabilities[0]

    return model_data
    # estimate_model_header_dict = {"Content-Type": "application/json", "Authorization": ESTIMATE_MODEL_SECRET}
    # estimate_model_endpoint = estimate_model_endpoint
    # vehicle_information = {
    #     "vin": vin,
    #     "sale_date": current_date.strftime("%Y-%m-%d"),
    #     "condition_grade": condition_grade,
    #     "odometer_mi": odometer_mi,
    #     "auction_state": state,
    #     "trim": trim,
    #     "drivable_indicator": drivable_indicator,
    #     "client_floor_price": client_floor_price,
    #     "client_name": client_name,
    # }

    # estimate_model_response = requests.post(estimate_model_endpoint, data=json.dumps({"vehicles": [vehicle_information]}), headers=estimate_model_header_dict, verify=False)
    # if estimate_model_response.json()["results"][0]["result"]["results"][0]["price"] == None:
    #     raise ValueError("Estimate Model API returned a None value for price")
    
    # prices_and_probabilities = [(
    #     result["result"]["results"][0]["price"],
    #     result["result"]["results"][0]["predicted_prob"],
    #     result["result"]["results"][0]["trim_match"],
    #     result["result"]["results"][0]["price_low"],
    #     result["result"]["results"][0]["price_high"],
    #     )
    #     for result in estimate_model_response.json()["results"]
    # ]

    # model_data = (current_date.strftime("%Y-%m-%d"),) + prices_and_probabilities[0]

    # return model_data

def snowflake_query(vin, queries):
    
    response = helper.get_snowflake_query_data(vin)
    print(f"response: {response}")
    return response

    # conn = snowflake.connector.connect(
    #     user="SNOWFLAKE_USER_NAME",
    #     password=SNOWFLAKE_PASSWORD,
    #     account="123",
    #     role="integration",
    #     warehouse="CONSUMER_WAREHOUSE",
    #     database=SNOWFLAKE_DATABASE,
    #     schema="REPORTING_SCHEMA",
    #     session_parameters={"QUERY_TAG": "Estimator Tool Streamlit App"}
    # )
    # cur = conn.cursor()
    # results_list = []
    # for query in queries:
    #     cur.execute(query)
    #     results = cur.fetchall()
    #     results_list.append(results)
    # cur.close()
    # conn.close()
    # return results_list

def calculate_depreciation(df):
    if len(df) > 0:
        depreciation = (df["valuation"].iloc[-1] - df["valuation"].iloc[0]) / len(df)
        return round(depreciation)
    else:
        return 0

@st.cache_data(ttl=60 * 60 * 24, show_spinner=False, max_entries=10)
def process_data(vin, condition_grade, odometer, state, drivable_indicator, client_floor_price, client_name=None):
    try:
        year, make, model, trim = get_vehicle_description(vin)
        estimate_model_response = estimate_model_api_call(vin, condition_grade, odometer, state, trim, drivable_indicator, client_floor_price, client_name)
        print(f"estimate_model_response: {estimate_model_response}")
        estimate_model_response_df = pd.DataFrame([estimate_model_response], columns=["date", "valuation", "probability", "trim_match", "price_low", "price_high"])
        print(f"estimate_model_response_df: {estimate_model_response_df}")
        vin8_10 = vin[:8] + "_" + vin[9]
        print(f"vin8_10: {vin8_10}")
        snowflake_data = snowflake_query(vin,
            [
                f"SELECT VIN8_10, RETENTION_BAND, PROBABILITY FROM PRICE_ESTIMATOR_SOLD_PERCENTAGE WHERE VIN8_10 = '{vin8_10}';",
                f"SELECT TIMEFRAME, DATE, RELATIVE_VALUE_SCALE FROM PRICE_ESTIMATOR_MAKE_MODEL_GRAPH WHERE MAKE_MODEL = '{make.upper()}:{model.upper()}';",
                f"SELECT TIMEFRAME, DATE, PERCENTAGE_FROM_BASELINE, MARKET_SEGMENT FROM PRICE_ESTIMATOR_MARKET_SEGMENT_GRAPH WHERE MAKE = '{make.upper()}' AND MODEL = '{model.upper()}' AND MODEL_YEAR = '{year}';",
                "SELECT TIMEFRAME, DATE, PERCENTAGE_FROM_BASELINE, MARKET_SEGMENT FROM PRICE_ESTIMATOR_MARKET_SEGMENT_GRAPH WHERE MARKET_SEGMENT = 'Overall';",
            ]
        )
        print(f"snowflake_data: {snowflake_data}")

        if snowflake_data[2]:
            segment = snowflake_data[2][0][3]
            market_segment_index_df = pd.DataFrame(snowflake_data[2], columns=["timeframe", "date", "percentage_from_baseline", "market_segment"])
        else:
            segment = "Overall"
            market_segment_index_df = pd.DataFrame(snowflake_data[3], columns=["timeframe", "date", "percentage_from_baseline", "market_segment"])
        market_segment_index_df = market_segment_index_df.sort_values(by=["date"]).reset_index(drop=True)
        market_segment_index_df["percentage_from_baseline"] = market_segment_index_df["percentage_from_baseline"] / 100
        market_segment_index_df["date"] = market_segment_index_df["date"] - pd.Timedelta(days=1)  # just trying to make the altair chart line up the x axis with the points...not ideal, but not a huge deal to have sunday as start of week instead of monday
        market_segment_index_df["date"] = pd.to_datetime(market_segment_index_df["date"]).apply(lambda x: x.replace(hour=5))  # only here so that when altair tries to convert to local timezone, we don't end up on wrong date. Temporary solution?

        mm_index_df = pd.DataFrame(snowflake_data[1], columns=["timeframe", "date", "relative_value_scale"])
        mm_index_df["valuation"] = mm_index_df["relative_value_scale"] * estimate_model_response_df["valuation"].iloc[-1]
        mm_index_df["valuation"] = mm_index_df["valuation"].round()
        mm_index_df = mm_index_df.sort_values(by=["date"]).reset_index(drop=True)
        mm_index_df["date"] = mm_index_df["date"] - pd.Timedelta(days=1)
        mm_index_df["date"] = pd.to_datetime(mm_index_df["date"]).apply(lambda x: x.replace(hour=5))

        depreciation_results = mm_index_df.groupby("timeframe").apply(calculate_depreciation)

        retention_cdfs_df = pd.DataFrame(snowflake_data[0], columns=["vin8_10", "retband", "prob"])[["retband", "prob"]]
        retention_cdfs_df["price"] = retention_cdfs_df["retband"] * estimate_model_response_df["valuation"].iloc[-1]
        retention_cdfs_df["price"] = retention_cdfs_df["price"].round()
        retention_cdfs_df["formatted_price"] = retention_cdfs_df["price"].apply(lambda x: f"${round(x, -2)/1000:.1f}k")
        retention_cdfs_df["prob"] = retention_cdfs_df["prob"].astype(str)
        retention_cdfs_df = retention_cdfs_df.sort_values(by=["retband"]).reset_index(drop=True)

    except Exception as e:
        logging.error(f"Error in process_data: {e}")
        st.error(
            "Oops! It looks like the VIN you entered cannot be processed. Please go [here](https://google.com) to leave feedback and report the issue."
        )
        st.stop()

    return {
        "estimate_model_data": estimate_model_response_df,
        "market_segment_data": market_segment_index_df,
        "mm_data": mm_index_df,
        "depreciation": depreciation_results,
        "retention_cdfs_data": retention_cdfs_df,
        "segment": segment,
        "year": year,
        "make": make,
        "model": model,
        "trim": trim,
    }

def plot_data(df, x_field, y_field, center_y_on_zero=False, x_axis_title=None, y_axis_title=None, y_axis_format=None):
    if center_y_on_zero:
        max_abs_val = df[y_field].abs().max()
        y_scale = alt.Scale(domain=[-max_abs_val - 0.01, max_abs_val + 0.01])
    else:
        min_val, max_val = df[y_field].min(), df[y_field].max()
        padding = (max_val - min_val) * 0.1
        y_scale = alt.Scale(domain=[min_val - padding, max_val + padding])

    x_axis = alt.X(x_field,title=None,axis=alt.Axis(grid=True,labelAngle=-50,format="%Y-%m-%d",labelFont="Inter",labelFontSize=10,tickCount=len(df[x_field])))

    if y_axis_format:
        y_axis = alt.Y(y_field,scale=y_scale,title=None,axis=alt.Axis(format=y_axis_format, labelFont="Inter", labelFontSize=10))
    else:
        y_axis = alt.Y(y_field,scale=y_scale,title=None,axis=alt.Axis(labelFont="Inter", labelFontSize=10))

    line = alt.Chart(df).mark_line(color="#59aab6", tooltip=False, interpolate="monotone").encode(
        x=x_axis,y=y_axis
        ).properties(height=340, width=700)
        
    points = alt.Chart(df).mark_circle(stroke="#59aab6", strokeWidth=2, fill="white", opacity=1).encode(
            x=x_axis, y=y_axis, tooltip=[alt.Tooltip(x_field, title=x_axis_title), alt.Tooltip(y_field, title=y_axis_title, format=y_axis_format)]
        )

    chart = line + points

    if center_y_on_zero:
        zero_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#053038", strokeWidth=1.5, strokeDash=[5, 2]).encode(y="y:Q")
        chart = alt.layer(chart, zero_line)
        
    st.altair_chart(chart, theme=None, use_container_width=True)

def calculate_user_circle_position(df, client_floor_price):
    if client_floor_price is None:
        return None

    rounded_floor_price = round(client_floor_price / 100) * 100
    rounded_prices = df["price"].apply(lambda x: round(x / 100) * 100).tolist()

    if rounded_floor_price < rounded_prices[0]:
        return None
    elif rounded_floor_price > rounded_prices[-1]:
        return None
    else:
        for i in range(1, len(rounded_prices)):
            if rounded_floor_price == rounded_prices[i - 1]:
                return i
            elif rounded_prices[i - 1] < rounded_floor_price < rounded_prices[i]:
                return round(i + (rounded_floor_price - rounded_prices[i - 1]) / (rounded_prices[i] - rounded_prices[i - 1]), 2)
            elif rounded_floor_price == rounded_prices[i]:
                return i + 1
        return None

def plot_sold_percentage(df, client_floor_price):
    user_circle_position = calculate_user_circle_position(df, client_floor_price)

    circles_df = pd.DataFrame(
        {
            "Position": [1, 2, 3, 4, 5, 6, 7],
            "Value": [0] * 7,
            "Price": df["formatted_price"].tolist(),
            "Probability": df["prob"].tolist(),
        }
    )

    line = alt.Chart(pd.DataFrame({"x": [1, 7], "y": [0, 0]})).mark_line(color="#dcdee1").encode(
            x=alt.X("x:Q", axis=alt.Axis(labels=False, title=None, ticks=False, domain=False)),
            y=alt.Y("y:Q", axis=alt.Axis(labels=False, title=None, ticks=False, domain=False))
        )
    
    points = alt.Chart(circles_df).mark_point(color="#dcdee1", size=100, fill="white", opacity=1, tooltip=False).encode(
            x=alt.X("Position:Q", axis=alt.Axis(labels=False, title=None, ticks=False, domain=False)),
            y=alt.Y("Value:Q", axis=alt.Axis(labels=False, title=None, ticks=False, domain=False))
        )
    
    text_above = alt.Chart(circles_df).mark_text(fontSize=12, font="Inter", dy=-18, tooltip=False).encode(x="Position:Q", y="Value:Q", text=alt.Text("Price:N"))
    text_below = alt.Chart(circles_df).mark_text(fontSize=12, font="Inter", dy=18, tooltip=False).encode(x="Position:Q", y="Value:Q", text=alt.Text("Probability:Q", format=".0%"))

    user_circle_outline = alt.Chart(pd.DataFrame({"x": [user_circle_position], "y": [0]})).mark_circle(size=120,opacity=1,stroke="#59aab6",strokeWidth=2,fill="white",tooltip=False).encode(
        x=alt.X("x:Q", axis=alt.Axis(labels=False, title=None, ticks=False, domain=False)),
        y=alt.Y("y:Q",axis=alt.Axis(labels=False, title=None, ticks=False, domain=False))
    )
    
    user_circle_dot = alt.Chart(pd.DataFrame({"x": [user_circle_position], "y": [0]})).mark_circle(color="#59aab6", size=10, opacity=1, tooltip=False).encode(
        x=alt.X("x:Q", axis=alt.Axis(labels=False, title=None, ticks=False, domain=False)),
        y=alt.Y("y:Q", axis=alt.Axis(labels=False, title=None, ticks=False, domain=False))
    )

    chart = alt.layer(line, points, text_above, text_below, user_circle_outline, user_circle_dot).properties(height=70, width=600).configure_axis(grid=False, domain=False, ticks=False, labels=False).configure_view(strokeWidth=0)
    
    st.altair_chart(chart, use_container_width=True)


def depreciation_message(depreciation, year, make, model, timeframe):
    if depreciation > 0:
        return st.markdown(
            f'<p style="font-family:Inter; color: #053038; font-size: 15px; margin-bottom: 2px; margin-top:-2px;">Based on the last {timeframe.lower()}, {year} {make} {model}s are '
            f'<span style="color: green; font-weight:500;">appreciating by ${depreciation}</span> per week.',
            unsafe_allow_html=True,
        )

    elif depreciation < 0:
        return st.markdown(
            f'<p style="font-family:Inter; color: #053038; font-size: 15px; margin-bottom: 2px; margin-top:-2px;">Based on the last {timeframe.lower()}, {year} {make} {model}s are '
            f'<span style="color: #bf2828; font-weight:500;">depreciating by ${abs(depreciation)}</span> per week.',
            unsafe_allow_html=True,
        )
    else:
        return st.markdown(
            f'<p style="font-family:Inter; color: #053038; font-size: 15px; margin-bottom: 2px; margin-top:-2px;">Based on the last {timeframe.lower()}, {year} {make} {model}s are not appreciating or depreciating.',
            unsafe_allow_html=True,
        )

def validate_inputs(vin, odometer, condition_grade, auction_state, drivable_indicator, client_floor_price=None):
    if not vin or len(vin) != 17:
        st.error("Please enter a valid 17 character VIN")
        st.stop()
    if odometer is None or odometer < 0 or odometer > 500000 or type(odometer) != int:
        st.error("Please enter a valid odometer mileage")
        st.stop()
    if condition_grade is None or condition_grade < 0.0 or condition_grade > 5.0 or type(condition_grade) != float:
        st.error("Please enter a valid condition grade")
        st.stop()
    if not auction_state or auction_state not in map(str.upper, state_names):
        st.error("Please enter a valid auction state")
        st.stop()
    if not drivable_indicator or drivable_indicator not in ["DRIVABLE", "NOT DRIVABLE"]:
        st.error("Please enter a valid drivable option")
        st.stop()
    if client_floor_price is not None and (client_floor_price < 1000 or client_floor_price > 150000 or type(client_floor_price) != int):
        st.error("Please enter a valid desired floor price or leave blank")
        st.stop()

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def on_selectbox_change(timeframe):
    if st.session_state.timeframe_filter != timeframe:
        st.session_state.timeframe_filter = timeframe

def sidebar():
    with st.sidebar:
        helper.header("Price Estimator", "https://google.com")

        with st.form(key="input_form", border=True):
            st.markdown(
                '<p style="font-family:Inter; color: #053038; font-size: 18px; font-weight: 600; margin-bottom: 10px;">Price My Car</p>',
                unsafe_allow_html=True,
            )

            vin = st.text_input("VIN", placeholder="VIN (2004 Earliest Year)", max_chars=17, help="Please enter a valid 17 character VIN").upper()
            odometer = st.number_input("Odometer (Miles)",min_value=0,max_value=500000,step=1000,value=50000,help="Please enter a number between 0 and 500,000",placeholder="0 - 500,000")
            condition_grade = st.number_input("Condition Grade",min_value=0.0,max_value=5.0,step=0.1,value=3.0,placeholder="0.0 - 5.0",help="Please enter a number between 0.0 and 5.0",format="%.1f")
            state = st.selectbox("Location (State)", state_names).upper()
            drivable_indicator = st.radio("Drivable", ["Yes", "No"], horizontal=True)
            drivable_indicator = {"Yes": "DRIVABLE", "No": "NOT DRIVABLE"}[drivable_indicator]
            client_floor_price = st.number_input("Desired Floor Price (Optional)",min_value=1000,max_value=150000,step=500,value=None,placeholder="$1,000 - $150,000",help="Optional input: Please enter a number between 1,000 and 150,000 or leave blank",)
            get_estimate = st.form_submit_button("Get Estimate")

    if get_estimate:
        st.session_state["form_data"] = True

    return vin, condition_grade, odometer, state, drivable_indicator, client_floor_price, get_estimate

def main():
    helper.css_override()

    vin, condition_grade, odometer, state, drivable_indicator, client_floor_price, get_estimate = sidebar()
    client_name = f"PE:Your Name"[:30]

    if get_estimate or st.session_state.form_data:
        validate_inputs(vin, odometer, condition_grade, state, drivable_indicator, client_floor_price)

        data = process_data(vin, condition_grade, odometer, state, drivable_indicator, client_floor_price, client_name)

        estimate_model_data = data["estimate_model_data"]
        valuation_text = "${:,.0f}".format(estimate_model_data["valuation"].iloc[-1])
        price_low_text = "${:,.0f}".format(estimate_model_data["price_low"].iloc[-1])
        price_high_text = "${:,.0f}".format(estimate_model_data["price_high"].iloc[-1])
        odometer_text = "{:,.0f}".format(odometer)
        retention_cdfs_data = data["retention_cdfs_data"]
        segment = data["segment"]
        year = data["year"]
        make = data["make"]
        model = data["model"]
        trim = data["trim"]
        trim_text = f"{trim}" if trim else "No Trim Information Available"
        market_segment_data_unfiltered = data["market_segment_data"]
        market_segment_data = market_segment_data_unfiltered[market_segment_data_unfiltered["timeframe"] == st.session_state.timeframe_filter]
        mm_data_unfiltered = data["mm_data"]
        mm_data = mm_data_unfiltered[mm_data_unfiltered["timeframe"] == st.session_state.timeframe_filter]

        if len(data["depreciation"]) > 0:
            depreciation = data["depreciation"][st.session_state.timeframe_filter]
        else:
            depreciation = 0

        col1, col2, col3, col4 = st.columns([1, 6, 6, 1])
        with col2:
            wholesale_estimate_container = st.container(border=True)
            with wholesale_estimate_container:
                st.markdown("")
                left_col, right_col = st.columns([1, 1])

                with left_col:
                    st.markdown(
                        f"""
                        <div class="valuationText">
                        <p style="text-align: center; max-width: 100%; margin: 0 auto; font-family:Inter; color: #053038; margin-bottom: 0px; padding-top:0px; line-height: 55px;">{valuation_text}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<p style="text-align: center; max-width: 100%; margin: 0 auto; font-family:Inter; color: #053038; font-size: 12px; margin-bottom: 2px; font-weight: 500">Wholesale Estimate</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<p style="text-align: center; max-width: 100%; margin: 0 auto; font-family:Inter; color: #053038; font-size: 11px; margin-bottom: 2px; font-weight: 400">Low: {price_low_text} | High: {price_high_text}</p>',
                        unsafe_allow_html=True,
                    )

                with right_col:
                    st.markdown(
                        f'<p style="font-family:Inter; color: #053038; font-size: 14px; font-weight: 600; margin-bottom: 2px; margin-top: 5px;">{year} {make} {model}</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<p style="font-family:Inter; color: #053038; font-size: 12px; margin-bottom: 2px">{trim_text}</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<p style="font-family:Inter; color: #053038; font-size: 12px; margin-bottom: 2px">{odometer_text} miles</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<p style="font-family:Inter; color: #053038; font-size: 12px; margin-bottom: 27px;">VIN: {vin}</p>',
                        unsafe_allow_html=True,
                    )
                st.markdown("")

        with col3:
            sold_percentage_container = st.container(border=True)
            with sold_percentage_container:
                st.markdown("")
                left_col, right_col = st.columns([1, 1])

                with left_col:
                    st.markdown(
                        f'<p style="font-family:Inter; color: #053038; font-size: 16px; font-weight: 600;">Sold Percentage</p>',
                        unsafe_allow_html=True,
                    )

                with right_col:
                    encoded_img = img_to_bytes("src/assets/hollow_circle.png")
                    st.markdown(
                        f"""
                        <div class="desiredFloorPriceDiv" style="vertical-align:middle; margin-bottom:16px; text-align:right;">
                        <img src="data:image/png;base64,{encoded_img}" style="display:inline; width:18px; margin-right:5px;">
                        <p style="font-family:Inter; color: #59aab6; font-size: 12px; font-weight: 600; display:inline;">Desired Floor Price</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                plot_sold_percentage(retention_cdfs_data, client_floor_price)

        col1, col2, col3 = st.columns([1, 12, 1])
        with col2:
            wholesale_market_trends_container = st.container(border=False)
            with wholesale_market_trends_container:
                st.markdown(
                    f'<p style="font-family:Inter; color: #053038; font-size: 18px; font-weight: 600; margin-bottom: 2px;">Wholesale Market Trends</p>',
                    unsafe_allow_html=True,
                )
                depreciation_message(depreciation, year, make, model, st.session_state.timeframe_filter)
        st.markdown("")

        col1, col2, col3, col4 = st.columns([1, 6, 6, 1])
        with col2:
            make_model_container = st.container(border=True)
            with make_model_container:
                st.markdown(
                    f'<p style="font-family:Inter; color: #053038; font-size: 16px; font-weight: 600; margin-top: 10px; margin-bottom: 8px;">{year} {make} {model}</p>',
                    unsafe_allow_html=True,
                )
                if mm_data.empty:
                    st.error("No historical data is available for this vehicle.")
                else:
                    plot_data(mm_data, "date", "valuation", x_axis_title="Date", y_axis_title="Valuation", y_axis_format="$,.0f")
        with col3:
            market_segment_container = st.container(border=True)
            with market_segment_container:
                st.markdown(
                    f'<p style="font-family:Inter; color: #053038; font-size: 16px; font-weight: 600; margin-top: 10px; margin-bottom: 8px;">{segment} Market</p>',
                    unsafe_allow_html=True,
                )
                plot_data(market_segment_data, "date", "percentage_from_baseline", center_y_on_zero=True, x_axis_title="Date", y_axis_title="Percentage From Baseline", y_axis_format=".1%")

        col1, col2, col3, col4 = st.columns([1, 6, 6, 1])
        with col2:
            st.selectbox("Date Range:", ["4 Weeks", "8 Weeks", "12 Weeks"], index=1, label_visibility="collapsed", key="timeframe_filter", format_func=lambda x: "Last " + x, on_change=lambda: on_selectbox_change(st.session_state.timeframe_filter))


if __name__ == "__main__":
    main()