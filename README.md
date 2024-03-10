# Price Estimator Tool

This tool is meant to help customers effectively price their vehicles. It combines information about what the vehicles current 'worth' is, along with data about the likelihood at selling at different price points, as well as historical trends for the vehicle and the broader market performance to understand the costs associated with not selling the vehicle quickly (depreciation metrics). 

I am using mock data, but this is meant to illustrate how this kind of data can be utilized in a front-end interface. In a production environment, this tool would connect to internal APIs, external APIs, and internal databases to gather, transform, and present data to users. I have kept the code for how it would work not using mock data for reference.

I originally developed this tool in HTML, CSS, and JavaScript and connected to a serverless function I wrote in Python to handle the API calls and database queries. This version in Streamlit was more challenging to get to function in a similar way, but was successful after learning more about using Streamlit's session state.

To run, just download and use `streamlit run src/app.py`

![image](https://github.com/dillonalexander/Price-Estimator-Tool/assets/101664530/0678b50d-f774-4b46-ba67-b50018c01d28)
