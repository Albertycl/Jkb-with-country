# from flask import Flask
from datetime import timedelta
from flask import Blueprint
from model import db, all_monitoring_items_detail
from config import DevConfig
from flask import Flask, render_template, request, jsonify
import requests
import datetime
import json
import time
import datetime
from config import DevConfig
from flask_cors import CORS, cross_origin


a20_alert_threshold = Blueprint("a20_alert_threshold", __name__)




# **********************************************************************
@a20_alert_threshold.route("/get_alert_threshold")
@a20_alert_threshold.route("/get_alert_threshold/")
def get_alert_threshold():


    all_rows_for_all_monitoring_items_detail=all_monitoring_items_detail.query.all()
    for each_row in all_rows_for_all_monitoring_items_detail:
        each_row.alert_threshold=""
        each_row.threshold_as_a_list=""
        each_row.link_for_edit_threshold=""
    db.session.commit()


    str_jkb_token = requests.get(f"http://127.0.0.1:5065/jkb_api_request_token_new_version").text
    

    headers = {'token': str(str_jkb_token)}
    # task_id=132303549
    list_all_the_values=[]
    all_rows_for_all_monitoring_items_detail=all_monitoring_items_detail.query.all()
    for each_row_is_monitor_item in all_rows_for_all_monitoring_items_detail:
        str_all_the_alerts=""
        task_id=each_row_is_monitor_item.task_id
        task_name=each_row_is_monitor_item.task_name
        dict_key_id_value_alerts={}
        list_all_the_values=[]
        dict_alert_list=requests.get(f"https://v6-api.jiankongbao.com/siteapi/tasks/threshold/{task_id}", headers=headers).json()
        link_for_edit_threshold=f"https://monitoring.cloudwise.com/monitoring/#/create/tcp?task_id={task_id}"
        try:
            list_each_alert=dict_alert_list["data"]
            for each_alert_in_this_monitor_id in list_each_alert:
                alert_threshold=each_alert_in_this_monitor_id["value"]
                list_all_the_values.append(alert_threshold)
            dict_key_id_value_alerts[task_id]=list_all_the_values
            list_for_all_the_threshold_for_this_sensor=dict_key_id_value_alerts[task_id]
            for each_alert in list_for_all_the_threshold_for_this_sensor:
                print(f"each_alert={each_alert} / task_id={task_id}")
                str_all_the_alerts=str(list_for_all_the_threshold_for_this_sensor)
                each_row_is_monitor_item.threshold_as_a_list=str_all_the_alerts
                db.session.commit()
                if each_alert!="":
                    each_row_is_monitor_item.alert_threshold=each_alert
                    each_row_is_monitor_item.link_for_edit_threshold=link_for_edit_threshold
                    db.session.commit()
                
        except Exception as error:
            msg=dict_alert_list["msg"]
            print(f"error={error} / task_id={task_id} / msg={msg}")
            each_row_is_monitor_item.alert_threshold=msg
            each_row_is_monitor_item.threshold_as_a_list=str_all_the_alerts      
            each_row_is_monitor_item.link_for_edit_threshold=link_for_edit_threshold
            db.session.commit()


    return "1"



# # **********************************************************************
# @a20_alert_threshold.route("/debug_get_alert_threshold")
# @a20_alert_threshold.route("/debug_get_alert_threshold/")
# @a20_alert_threshold.route("/debug_get_alert_threshold/<task_id>")
# def debug_get_alert_threshold(task_id):
#     str_jkb_token = requests.get(f"http://127.0.0.1:5065/jkb_api_request_token_new_version").text
#     headers = {'token': str(str_jkb_token)}
#     # task_id=132303549
#     all_rows_for_all_monitoring_items_detail=all_monitoring_items_detail.query.all()
#     # for each_row_is_monitor_item in all_rows_for_all_monitoring_items_detail:
#         # alert_threshold=each_row_is_monitor_item.alert_threshold
#         # print(f"alert_threshold={alert_threshold}")
#         # id=each_row_is_monitor_item.id
#         # if type(alert_threshold)!=str:
#         #     alert_threshold=each_row_is_monitor_item.alert_threshold
#         #     print("id={id}")
#         # task_id=each_row_is_monitor_item.task_id
#     # task_name=each_row_is_monitor_item.task_name
#     dict_alert_list = requests.get(f"https://v6-api.jiankongbao.com/siteapi/tasks/threshold/{task_id}", headers=headers).json()
#     list_something=dict_alert_list["data"]
#     for each_threshold in list_something:
#         print(f"each_threshold={each_threshold}\n\n")
#         value=each_threshold["value"]
#         task_type=each_threshold["task_type"]
#         print(f"task_id={task_id} / value={value} / task_type={task_type}")
 

#     return "1"


# **********************************************************************
@a20_alert_threshold.route("/axios_threshold")
@a20_alert_threshold.route("/axios_threshold/")
def axios_threshold():
    list_all_the_data_in_all_monitoring_items_detail_table = all_monitoring_items_detail.query.order_by(all_monitoring_items_detail.task_name.desc()).all()
    list_all_the_data_in_all_monitoring_items_detail_table = [data.serialize_for_threshold for data in list_all_the_data_in_all_monitoring_items_detail_table]
    return jsonify(list_all_the_data_in_all_monitoring_items_detail_table)
