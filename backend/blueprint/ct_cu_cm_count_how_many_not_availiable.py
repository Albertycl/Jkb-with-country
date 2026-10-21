# from flask import Flask
from model import db, all_monitoring_items_detail
from config import DevConfig
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import jsonify
import time,datetime,json,requests
from config import DevConfig
from flask_cors import CORS, cross_origin
from flask import Blueprint
from datetime import timedelta

ct_cu_cm_count_how_many_not_availiable = Blueprint("ct_cu_cm_count_how_many_not_availiable", __name__)


# **********************************************************************
# @ct_cu_cm_count_how_many_not_availiable.route("/count_ct_cu_cm")
# @ct_cu_cm_count_how_many_not_availiable.route("/count_ct_cu_cm/")
# @ct_cu_cm_count_how_many_not_availiable.route("/count_ct_cu_cm/<task_id>/<last_check_time>")
def count_ct_cu_cm(task_id=1777971, last_check_time=1609862399):
    str_jkb_token = requests.get(f"http://127.0.0.1:5065/jkb_api_request_token_new_version").text
    headers = {'token': str(str_jkb_token)}
    response_for_checking_ct_cu_cm = requests.get(f"https://v6-api.jiankongbao.com/siteapi/data/snapshot/time?task_id={task_id}&check_time={last_check_time}", headers=headers).text
    #####################################################################################
    dic_response = json.loads(response_for_checking_ct_cu_cm)
    whole_row_when_task_id_matches = all_monitoring_items_detail.query.filter(
        all_monitoring_items_detail.task_id == task_id).first()
    if whole_row_when_task_id_matches != None:
        try:
            count_how_many_isp_cu_not_available = 0
            count_how_many_isp_ct_not_available = 0
            count_how_many_isp_cmi_not_available = 0
            count_how_many_isp_others_not_available = 0
            for key_1, value_2 in dic_response.items():
                for each_element in value_2:
                    # print(f"each_element={each_element}")
                    resp_status = each_element["check_result"]["resp_status"]
                    resp_result = each_element["check_result"]["resp_result"]
                    monitor_name = each_element["monitor_name"]
                    if resp_result == 0:
                        # print(f"monitor_name={monitor_name}")
                        if "聯通" in monitor_name:
                            count_how_many_isp_cu_not_available = count_how_many_isp_cu_not_available + 1
                        elif "電信" in monitor_name:
                            count_how_many_isp_ct_not_available = count_how_many_isp_ct_not_available + 1
                        elif "移動" in monitor_name:
                            count_how_many_isp_cmi_not_available = count_how_many_isp_cmi_not_available + 1
                        elif "联通" in monitor_name:
                            count_how_many_isp_cu_not_available = count_how_many_isp_cu_not_available + 1
                        elif "电信" in monitor_name:
                            count_how_many_isp_ct_not_available = count_how_many_isp_ct_not_available + 1
                        elif "移动" in monitor_name:
                            count_how_many_isp_cmi_not_available = count_how_many_isp_cmi_not_available + 1

                whole_row_when_task_id_matches.how_many_cu_not_available = count_how_many_isp_cu_not_available
                whole_row_when_task_id_matches.how_many_ct_not_available = count_how_many_isp_ct_not_available
                whole_row_when_task_id_matches.how_many_cm_not_available = count_how_many_isp_cmi_not_available
                whole_row_when_task_id_matches.how_many_other_isp_not_available = count_how_many_isp_others_not_available
                db.session.commit()
        except Exception as error:
            whole_row_when_task_id_matches.how_many_cu_not_available = "cannot count"
            whole_row_when_task_id_matches.how_many_ct_not_available = "cannot count"
            whole_row_when_task_id_matches.how_many_cmi_not_available = "cannot count"
            whole_row_when_task_id_matches.how_many_other_isp_not_available = "cannot count"
            db.session.commit()
    return "1"
