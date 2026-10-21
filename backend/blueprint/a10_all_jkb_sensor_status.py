# from flask import Flask
from model import db, all_monitoring_items_detail
# from flask import Flask
from flask_migrate import Migrate
from config import DevConfig
from flask import Flask, request,jsonify,Blueprint
import requests,datetime,json,time
from config import DevConfig
from flask_cors import CORS
import json

import datetime
from datetime import timedelta
from blueprint.b10_classification import b20_get_the_group_list_for_probes
from blueprint.ct_cu_cm_count_how_many_not_availiable import count_ct_cu_cm
from blueprint.e10_udpate_isp_for_which_country import e11_update_the_isp_for_this_country


a10_all_jkb_sensor_status = Blueprint("a10_all_jkb_sensor_status", __name__)

##################################################################################


@a10_all_jkb_sensor_status.route("/a10_trigger_jkb_api_to_get_status_for_all_the_sensors")
@a10_all_jkb_sensor_status.route("/a10_trigger_jkb_api_to_get_status_for_all_the_sensors/")
def a10_trigger_jkb_api_to_get_status_for_all_the_sensors():

    db.session.query(all_monitoring_items_detail).delete()
    db.session.commit()
    str_jkb_token = requests.get(f"http://127.0.0.1:5065/jkb_api_request_token_new_version").text
    headers = {'token': str(str_jkb_token)}
    data = '{"page_size":100,"current_page":1}'
    dict_task_list = requests.post(f"https://v6-api.jiankongbao.com/siteapi/tasks/list", headers=headers, data=data).text
    dict_task_list = json.loads(dict_task_list)
    dic_http_monitor = dict_task_list["pagination"]
    how_many_pages = dic_http_monitor["total_pages"]
    for index in range(how_many_pages):
        data = {}
        index = index+1
        data["page_size"] = 100
        data["current_page"] = index
        data = json.dumps(data)
        dict_task_list = requests.post(f"https://v6-api.jiankongbao.com/siteapi/tasks/list", headers=headers, data=data).json()
        list_data=dict_task_list["data"]

        for each_monitor_item in list_data:
            task_id = each_monitor_item["task_id"]
            task_name = each_monitor_item["task_name"]
            task_summary = each_monitor_item["task_summary"]
            monitor_target=task_summary.replace("http://","").replace("https://","").replace("tcp://","").split(":")[0].split("/")[0]
            group_id = each_monitor_item["group_id"]
            task_type = each_monitor_item["task_type"]
            paused_or_started = each_monitor_item["task_status"]
            two_means_hit_threshold = each_monitor_item["threshold_result"]
            last_resp_status = each_monitor_item["last_resp_status"]
            last_resp_time = each_monitor_item["last_resp_time"]
            last_check_time = each_monitor_item["last_check_time"]
            if last_resp_status=="不包含匹配內容":
                two_means_hit_threshold=2

            link_for_availability = f"https://monitoring.cloudwise.com/monitoring/#/taskdata/availability/base?task_id={task_id}&check_time={last_check_time}"
            link_for_snapshot = f"https://monitoring.cloudwise.com/monitoring/#/taskdetails/snapshot?page_name=timeList&task_id={task_id}&check_time={last_check_time}"
            link_for_response_time = f"https://monitoring.cloudwise.com/monitoring/#/taskdata/response/base?task_id={task_id}&check_time={last_check_time}"
  
            if paused_or_started!=3:
                last_check_time_readable=convert_sec_to_time(task_id,task_name,paused_or_started,last_check_time)
                whole_row_to_insert = all_monitoring_items_detail(task_id=task_id, task_name=task_name, task_summary=task_summary, group_id=group_id, task_type=task_type, link_for_availability=link_for_availability, link_for_snapshot=link_for_snapshot, link_for_response_time=link_for_response_time, paused_or_started=paused_or_started, two_means_hit_threshold=two_means_hit_threshold, last_resp_status=last_resp_status, last_resp_time=last_resp_time, last_check_time=last_check_time, last_check_time_readable=last_check_time_readable,monitor_target=monitor_target)
                db.session.add(whole_row_to_insert)
                db.session.commit()

    # a15_removing_the_domain_that_dont_want_to_monitor()


    b20_get_the_group_list_for_probes()
    e11_update_the_isp_for_this_country()
    # **********************************
    # b20_get_the_group_list_for_probes will trigger the below three functions
    # b30_update_group_in_table_all_monitoring_items_detail()
    # b40_convert_the_monitor_target_domain_name_in_table_all_monitoring_items_detail_to_ip()     
    # b50_convert_the_ip_to_infra()   

    return "1"


##################################################################################




##################################################################################

@a10_all_jkb_sensor_status.route("/a20_update_the_current_monitoring_status")
@a10_all_jkb_sensor_status.route("/a20_update_the_current_monitoring_status/")
def a20_update_the_current_monitoring_status():
    str_jkb_token = requests.get(f"http://127.0.0.1:5065/jkb_api_request_token_new_version").text
    headers = {'token': str(str_jkb_token)}
    data = '{"page_size":100,"current_page":1}'
    dict_task_list_response = requests.post(f"https://v6-api.jiankongbao.com/siteapi/tasks/list", headers=headers, data=data)
    dict_task_list = requests.post(f"https://v6-api.jiankongbao.com/siteapi/tasks/list", headers=headers, data=data).json()

    dic_http_monitor = dict_task_list["pagination"]
    how_many_pages = dic_http_monitor["total_pages"]
    for index in range(how_many_pages):
        # for index in range(1):
        data = {}
        index = index+1
        data["page_size"] = 100
        data["current_page"] = index
        data = json.dumps(data)
        dict_task_list = requests.post(f"https://v6-api.jiankongbao.com/siteapi/tasks/list", headers=headers, data=data).json()
        

        list_data=dict_task_list["data"]
        for each_monitor_item in list_data:
            task_id = each_monitor_item["task_id"]
            task_name = each_monitor_item["task_name"]
            # task_summary = each_monitor_item["task_summary"]
            # group_id = each_monitor_item["group_id"]
            # task_type = each_monitor_item["task_type"]
            paused_or_started = each_monitor_item["task_status"]
            two_means_hit_threshold = each_monitor_item["threshold_result"]
            last_resp_status = each_monitor_item["last_resp_status"]
            if last_resp_status=="不包含匹配內容":
                two_means_hit_threshold=2
            # if "成功" not in last_resp_status and "200" not in last_resp_status and "302" not in last_resp_status and "301" not in last_resp_status and paused_or_started==1:
                # print(f"task_id={task_id} / last_resp_status={last_resp_status} / two_means_hit_threshold={two_means_hit_threshold}")
            last_resp_time = each_monitor_item["last_resp_time"]
            last_check_time = each_monitor_item["last_check_time"]

            link_for_availability = f"https://monitoring.cloudwise.com/monitoring/#/taskdata/availability/base?task_id={task_id}&check_time={last_check_time}"
            link_for_snapshot = f"https://monitoring.cloudwise.com/monitoring/#/taskdetails/snapshot?page_name=timeList&task_id={task_id}&check_time={last_check_time}"
            link_for_response_time = f"https://monitoring.cloudwise.com/monitoring/#/taskdata/response/base?task_id={task_id}&check_time={last_check_time}"

            if paused_or_started!=3:  
                last_check_time_readable=convert_sec_to_time(task_id,task_name,paused_or_started,last_check_time)
                try:
                    row_when_url_matches = all_monitoring_items_detail.query.filter(all_monitoring_items_detail.task_id == task_id).first()
                    row_when_url_matches.link_for_availability = link_for_availability
                    row_when_url_matches.link_for_snapshot = link_for_snapshot
                    row_when_url_matches.link_for_response_time = link_for_response_time
                    row_when_url_matches.paused_or_started = paused_or_started
                    row_when_url_matches.two_means_hit_threshold = two_means_hit_threshold
                    row_when_url_matches.last_resp_status = last_resp_status
                    row_when_url_matches.last_resp_time = last_resp_time
                    row_when_url_matches.last_check_time = last_check_time
                    row_when_url_matches.last_check_time_readable = last_check_time_readable
                    row_when_url_matches.how_many_ct_not_available = "default_none"
                    row_when_url_matches.how_many_cu_not_available = "default_none"
                    row_when_url_matches.how_many_cm_not_available = "default_none"
                    row_when_url_matches.how_many_other_isp_not_available = "default_none"
                    db.session.commit()
                            
                except Exception as error:
                    print(f"in route a20_update_the_current_monitoring_status / task_id={task_id} / task_name={task_name} / error={error}")
                    
                        
    check_ct_cu_cm_how_many_not_available()

    return "1"

##################################################################################
def convert_sec_to_time(task_id,task_name,paused_or_started,input_is_sec):
    from datetime import datetime
    try:
        unit_time = int(input_is_sec)
        last_check_time_readable = datetime.utcfromtimestamp(unit_time)
        last_check_time_readable = last_check_time_readable +timedelta(hours=8)
    except Exception as error:
        print(f"in function convert_sec_to_time / task_id={task_id} / task_name={task_name} / paused_or_started={paused_or_started} / error={error}")
        last_check_time_readable="error"
    return last_check_time_readable

##################################################################################
# checking ct cu cm, how many not available
def check_ct_cu_cm_how_many_not_available():
    print(f"in function check_ct_cu_cm_how_many_not_available")
    whole_row_if_last_check_time_matches = all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold == 2, all_monitoring_items_detail.paused_or_started != 3).all()
    for each_row in whole_row_if_last_check_time_matches:
        task_id = each_row.task_id
        last_check_time = each_row.last_check_time
        count_ct_cu_cm(task_id,last_check_time)



##################################################################################
@a10_all_jkb_sensor_status.route("/a30_set_ct_cu_cm_not_available")
@a10_all_jkb_sensor_status.route("/a30_set_ct_cu_cm_not_available/")
def a30_set_ct_cu_cm_not_available():
    for_all_rows_in_table_all_monitoring_items_detail=all_monitoring_items_detail.query.all()
    for each_row in for_all_rows_in_table_all_monitoring_items_detail:
        each_row.how_many_ct_not_available=0
        each_row.how_many_cu_not_available=0
        each_row.how_many_cm_not_available=0
        each_row.how_many_other_isp_not_available=0
    db.session.commit()

    return "1"
