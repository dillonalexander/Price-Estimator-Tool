import streamlit as st
import pandas as pd
import datetime
from decimal import Decimal

def get_vehicle_resolver_token_data():

    token_response = {"status_code": 200, "access_token": "TOKEN"}
    return token_response

def get_vehicle_description_data(vin):
    if vin == '3C3CAXHG7KH528313':
        data = {'status_code': 200,
                'data': {'VINDescription': {'message': None, 'error': False, 
                        'result': {'vinProcessed': '3C3CAXHG7KH528313', 'validVin': True, 'year': '2019', 'make': 'Dodge', 'model': 'Charger', 
                                    'vehicles': [{'styleDescription': 'GT RWD', 'trim': 'GT', 'bodyType': 'Sedan'}]}}}}
    elif vin == '4F1C12HK1JU083649':
        data = {'status_code': 200,
                'data': {'VINDescription': {'message': None, 'error': False, 
                        'result': {'vinProcessed': '4F1C12HK1JU083649', 'validVin': True,  'year': '2018', 'make': 'Toyota', 'model': 'Camry', 
                                   'vehicles': [{'styleDescription': 'LE Auto (GS)', 'trim': 'LE', 'bodyType': 'Sedan'}]}}}}   
    elif vin == '1HTDW1CG4FKE42365':
        data = {'status_code': 200,
                'data': {'VINDescription': {'message': None, 'error': False, 
                        'result': {'vinProcessed': '1HTDW1CG4FKE42365', 'validVin': True,  'year': '2015', 'make': 'Ford', 'model': 'F-150', 
                                   'vehicles': [{'styleDescription': '2WD SuperCrew 157" Lariat', 'trim': 'Lariat', 'bodyType': 'Crew Cab'}]}}}}
    return data

def get_estimate_model_api_call_data(vin):
    if vin == '3C3CAXHG7KH528313':
        data = {'results': [{'status': 'OK', 
                             'result': {'results': [{'vin': '3C3CAXHG7KH528313', 'autograde': 3.3, 'price': 17565.0, 'price_low': 15685.0, 'price_high': 19444.0, 'predicted_prob': 0.7524103733020536, 'trim_match': True}]}}]}
    elif vin == '4F1C12HK1JU083649':
        data = {'results': [{'status': 'OK', 
                             'result': {'results': [{'vin': '4F1C12HK1JU083649', 'autograde': 4.0, 'price': 16934.0, 'price_low': 15646.0, 'price_high': 18223.0, 'predicted_prob': 0.9324711353307273, 'trim_match': True}]}}]}
    elif vin == '1HTDW1CG4FKE42365':
        data =  {'results': [{'status': 'OK', 
                              'result': {'results': [{'vin': '1HTDW1CG4FKE42365', 'autograde': 4.0, 'price': 23152.0, 'price_low': 20887.0, 'price_high': 25417.0, 'predicted_prob': 0.6822947499729123, 'trim_match': True}]}}]}
    return data

def get_snowflake_query_data(vin):
    if vin == '3C3CAXHG7KH528313':
        data = [
                [('3C3CAXHG_K', 0.95, Decimal('0.68')), ('3C3CAXHG_K', 0.9, Decimal('0.82')), ('3C3CAXHG_K', 1.1, Decimal('0.20')), ('3C3CAXHG_K', 1.0, Decimal('0.52')), ('3C3CAXHG_K', 0.85, Decimal('0.89')), ('3C3CAXHG_K', 1.15, Decimal('0.11')), ('3C3CAXHG_K', 1.05, Decimal('0.35'))], 
                [('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.9997), ('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 1.0124), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.0173), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.9997), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 1.0124), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.0173), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 1.0131999999999999), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 1.0048000000000001), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), 0.9926999999999999), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.9669), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.9997), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 1.0124), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.0173), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 1.0131999999999999), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 1.0048000000000001), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), 0.9926999999999999), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.9669), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), 0.9537), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), 0.9826), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), 0.9876999999999999), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 0.9902)], 
                [('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 0.9, 'Fullsize Car'), ('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.7, 'Fullsize Car'), ('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.8, 'Fullsize Car'), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.0, 'Fullsize Car'), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 2.7, 'Fullsize Car'), ('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 2.5, 'Fullsize Car'), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 2.6, 'Fullsize Car'), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.7, 'Fullsize Car'), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 1.8, 'Fullsize Car'), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.2, 'Fullsize Car'), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -0.4, 'Fullsize Car'), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.0, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 0.8, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.6, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.7, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), -0.1, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), -0.1, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), -1.6, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -2.2, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), -1.8, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), -2.1, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), -0.9, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), -0.1, 'Fullsize Car'), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 0.0, 'Fullsize Car')], 
                [('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), -0.7, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 1.1, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), -0.9, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), -1.7, 'Overall'), ('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 0.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), -0.8, 'Overall'), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.0, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), -1.5, 'Overall'), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), -0.3, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.8, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.0, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), -0.6, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -1.8, 'Overall'), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), -0.5, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), -0.6, 'Overall'), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 0.0, 'Overall'), ('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -0.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 1.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.0, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.7, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), -1.0, 'Overall')]]
    elif vin == '4F1C12HK1JU083649':
        data = [
                [('4F1C12HK_J', 1.0, Decimal('0.66')), ('4F1C12HK_J', 0.9, Decimal('0.89')), ('4F1C12HK_J', 1.05, Decimal('0.45')), ('4F1C12HK_J', 0.85, Decimal('0.93')), ('4F1C12HK_J', 0.95, Decimal('0.81')), ('4F1C12HK_J', 1.1, Decimal('0.28')), ('4F1C12HK_J', 1.15, Decimal('0.16'))], 
                [('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.9978), ('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.9872), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.9723999999999999), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.9978), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.9872), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.9723999999999999), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.9765), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.9815999999999999), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), 0.9737), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.9758), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.9978), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.9872), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.9723999999999999), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.9765), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.9815999999999999), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), 0.9737), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.9758), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), 0.9906999999999999), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), 1.0024), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), 1.0063), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 1.0093)], 
                [('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.3, 'Midsize Car'), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.0, 'Midsize Car'), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 1.9, 'Midsize Car'), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 1.8, 'Midsize Car'), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), 0.7, 'Midsize Car'), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.0, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -0.4, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), -1.1, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), -0.8, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), -0.5, 'Midsize Car'), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), -0.5, 'Midsize Car'), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 0.0, 'Midsize Car'),('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 0.2, 'Midsize Car'), ('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.5, 'Midsize Car'), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 2.7, 'Midsize Car'), ('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 3.0, 'Midsize Car'), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 2.8, 'Midsize Car'), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 2.5, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.5, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 1.8, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 1.7, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.3, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.7, 'Midsize Car'), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.7, 'Midsize Car')], 
                [('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 1.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.0, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.7, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), -1.0, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.8, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.0, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), -0.6, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -1.8, 'Overall'), ('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -0.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 1.1, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), -0.9, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), -1.7, 'Overall'), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.0, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), -1.5, 'Overall'), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), -0.3, 'Overall'), ('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), -0.7, 'Overall'), ('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 0.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), -0.8, 'Overall'), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), -0.5, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), -0.6, 'Overall'), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 0.0, 'Overall')]]
    elif vin == '1HTDW1CG4FKE42365':
        data = [
                [('1HTDW1CG_F', 0.9, Decimal('0.78')), ('1HTDW1CG_F', 0.85, Decimal('0.86')), ('1HTDW1CG_F', 1.1, Decimal('0.30')), ('1HTDW1CG_F', 0.95, Decimal('0.67')), ('1HTDW1CG_F', 1.05, Decimal('0.42')), ('1HTDW1CG_F', 1.0, Decimal('0.54')), ('1HTDW1CG_F', 1.15, Decimal('0.21'))], 
                [('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.987), ('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.9826999999999999), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.9688), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.987), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.9826999999999999), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.9688), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.9545999999999999), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.9520000000000001), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), 0.9529000000000001), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.9584999999999999), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.0), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.987), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.9826999999999999), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.9688), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.9545999999999999), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.9520000000000001), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), 0.9529000000000001), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.9584999999999999), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), 0.977), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), 0.9889), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), 0.9983), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 1.0103)], 
                [('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 1.4, 'Fullsize Pickup'), ('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.6, 'Fullsize Pickup'), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.0, 'Fullsize Pickup'), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 1.7, 'Fullsize Pickup'), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.2, 'Fullsize Pickup'), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.5, 'Fullsize Pickup'), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.4, 'Fullsize Pickup'), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -0.5, 'Fullsize Pickup'), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.0, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), -1.4, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), -2.0, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), -2.1, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -3.0, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), -2.5, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), -2.2, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), -1.1, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), -0.5, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 0.0, 'Fullsize Pickup'), ('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 2.0, 'Fullsize Pickup'), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 3.1, 'Fullsize Pickup'), ('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 2.5, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 0.5, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.0, 'Fullsize Pickup'), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), -0.8, 'Fullsize Pickup')], 
                [('8 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 1.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 1.0, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 29, 0, 0), 0.7, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 29, 0, 0), -1.0, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 5, 0, 0), 0.8, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 15, 0, 0), 0.0, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 19, 0, 0), -0.6, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -1.8, 'Overall'), ('4 Weeks', datetime.datetime(2024, 2, 26, 0, 0), 0.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 1, 22, 0, 0), -0.1, 'Overall'), ('8 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 1.1, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 5, 0, 0), -0.9, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 15, 0, 0), -1.7, 'Overall'), ('4 Weeks', datetime.datetime(2024, 2, 12, 0, 0), 0.0, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 8, 0, 0), -1.5, 'Overall'), ('12 Weeks', datetime.datetime(2023, 12, 25, 0, 0), -0.3, 'Overall'), ('4 Weeks', datetime.datetime(2024, 2, 19, 0, 0), 0.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 12, 0, 0), -0.7, 'Overall'), ('4 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 0.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 1, 1, 0, 0), -0.8, 'Overall'), ('8 Weeks', datetime.datetime(2024, 3, 4, 0, 0), 1.2, 'Overall'), ('12 Weeks', datetime.datetime(2024, 3, 4, 0, 0), -0.5, 'Overall'), ('12 Weeks', datetime.datetime(2024, 2, 26, 0, 0), -0.6, 'Overall'), ('12 Weeks', datetime.datetime(2023, 12, 18, 0, 0), 0.0, 'Overall')]]
    return data


def header(title: str, slack_url: str):
    st.markdown(
        f"""  
        <a href="{slack_url}" target="_blank">
            <button class="feedback-button">Feedback</button>
        </a>
        """,
        unsafe_allow_html=True,
    )
    st.image("src/assets/test-logo.png", width=140)
    st.header(title)
    st.markdown(
        '<hr style="border-top: 1px solid black; margin-top:12px; margin-bottom:12px;">',
        unsafe_allow_html=True,
    )
    
def css_override():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"');
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;500;600;700;800&family=Inter:wght@300;600&display=swap');
                
    * {
        font-family: 'Inter', sans-serif;
    }
                  
    /* remove ugly streamlit top bar */
    [data-testid="stDecoration"] {
        display: none;
    }

    p {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .valuationText p {
            font-size: 38px; 
            font-weight: 600;
        }

    [data-testid="stAlert"] p {
        white-space: normal;
        overflow: visible;
        text-overflow: clip;
    }

    /* How to modify border around containers in main content, but have to be explicit to modify already existing borders and not add new ones */ 
    [data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
        border-color: #e0e0e0;
        border-width: 2px;
    }
   
    /* forcing size for sidebar */
    [data-testid='stSidebar'][aria-expanded="true"]{
        min-width: 380px;
        max-width: 380px;
    }            

    /* forcing size for main content */
    .main > div:first-child {
        min-width: 1100px;
        max-width: 1550px;
        padding-bottom: 96px;
        padding-top: 75px;
    }

    .main [data-testid="stSelectbox"] [value] {
        font-size: 12px !important;
        margin-top: 4px !important;
    }
    .main [data-testid="stSelectbox"] {
        width: 150px !important;
    }

    /* collapsed button was hidden */
    [data-testid="collapsedControl"] {
        margin-top: 2.5rem;
        margin-left: 2.5rem;
    }

    /* reduce top padding for side bar */           
    [data-testid="stSidebarUserContent"] {
        padding-top: 1.5rem;
    }

    /* Integrated, nicer looking scrollbar.*/
    [data-testid="stSidebarContent"] {
        /*overflow-y: scroll;*/
        /*overflow-x: scroll;*/
        /*scrollbar-width: none;*/
        /*-ms-overflow-style: none;*/
        scrollbar-width: thin;
        scrollbar-color: rgb(240, 242, 246) transparent;
    }
    [data-testid="stSidebarContent"]::-webkit-scrollbar {
        /*width: 0;*/
        /*height: 0;*/
        width: 20px;
    }
    [data-testid="stSidebarContent"]::-webkit-scrollbar-track {
        background-color: rgb(240, 242, 246);
    }
    [data-testid="stSidebarContent"]::-webkit-scrollbar-thumb {
        background-color: rgb(240, 242, 246);
        border-radius: 20px;
    }
    
    /* sidebar hider position */
    [data-testid="baseButton-header"] {
        margin-top: 2.5rem;
    }    
    
    /* remove image fullscreen button */
    [data-testid="StyledFullScreenButton"] {
        display: none;
    }
    
    /* changing look of form's borders */
    [data-testid="stForm"] {
        border-radius: 12px;
        border-color: #d3d3d3;
        border-width: 2px;
    }   

    /* changing look for form's button */
    [data-testid="baseButton-secondaryFormSubmit"] {    
        background-color: #0c8599;
        color: white;     
        min-height: 2.8rem;
        min-width: 90%;
        max-width: 100%;
    }
    [data-testid="stFormSubmitButton"] {
        justify-content: center;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    [data-testid="stFormSubmitButton"] p{
        font-weight: 600;
    }
    /* removing input instructions */
    [data-testid="InputInstructions"] {
        display: none;
    }
    /* changing look of header in sidebar */     
    .stHeadingContainer h2 {
        font-size: 20px;
        padding-top: 0px;
        padding-bottom: 0px;
        margin-top: -5px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.4px;
        color: #053038;
    }
                
    [data-testid="stVerticalBlockBorderWrapper"] {
        padding-bottom: 0px;
        padding-top: 0px;
    }

    /* removing link text underlining in the feedback-button*/
    a { 
        text-decoration: none;
    }
    a:hover {
        text-decoration: none;
    }
    .feedback-button {
        align-items: center;
        background-color: #2b60af;
        border-radius: 4px;
        border: 0;
        box-shadow: rgba(1,60,136,.5) 0 -1px 3px 0 inset,rgba(0,44,97,.1) 0 3px 6px 0;
        box-sizing: border-box;
        color: #fff;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        line-height: 24px;
        margin: 0;
        min-height: 24px;
        max-height: 24px;
        min-width: 90px;
        max-width: 90px;
        padding: 16px 16px;
        text-align: center;
        user-select: none;
        transition: all .2s cubic-bezier(.22, .61, .36, 1);
        justify-content: center;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center; max-width: 100%; margin: 0 auto;
        margin-top: -1.7rem;
        margin-right: 0rem;
    }
    .feedback-button:hover {
        background-color: #224b89;
        transform: translateY(2px);
    }

    /* Mobile Device Styles */
    @media only screen and (max-width: 1400px) { 
    
        .valuationText p {
                font-size: 34px; 
            }
    
        [data-testid='stSidebar'][aria-expanded="true"]{
            min-width: 300px; /* Smaller sidebar for mobile */
            max-width: 300px;
        }

        [data-testid="baseButton-secondaryFormSubmit"] {    
        background-color: #0c8599;
        color: white;     
        min-width: 100%;
        max-width: 100%;
        padding: 0
        }

        .feedback-button {
        font-size: 12px;
        padding: 14px 14px;
        margin-right: -1rem;
        }

        [data-testid="stSidebarUserContent"] {
        padding-bottom: 24px;
        }

        [data-testid="stWidgetLabel"] {
            margin-top: -8px;
        }

        [data-testid="stWidgetLabel"] {
            margin-bottom: 0px;
        }
        
        .stMarkdown, .stTextInput, .stSelectbox, .stRadio {
            font-size: 12px; /* Smaller font size for mobile - not really working yet, likely due to specifying css elsewhere, declare explicit classes in st.markdown from now on.*/
        } 
        .stHeadingContainer h2 {
            font-size: 18px; /* Smaller heading size for mobile */
        }
        
    }


    @media only screen and (max-width: 1200px) {
        .main > div:first-child {
            min-width: 900px;
            max-width: 1150px;
            padding-left: 20px;
            padding-right: 20px;
        }

        .valuationText p {
                font-size: 32px; 
        }
        
    }

    @media only screen and (max-width: 640px) {
        .main > div:first-child {
            min-width: 550px;
            max-width: 550px;
            padding-left: 30px;
            padding-right: 30px;
        }

        p {
            white-space: normal;
            overflow: visible;
            text-overflow: clip;
        }
    } 

    @media only screen and (orientation: portrait) and (max-width: 640px) {
        .main > div:first-child {
            min-width: 400px;
            max-width: 400px;
            padding-left: 30px;
            padding-right: 30px;
            overflow-x: hidden;
        }

        p {
            white-space: normal;
            overflow: visible;
            text-overflow: clip;
        }
    } 

    </style>
    """,
        unsafe_allow_html=True,
    )
