from flask import Blueprint
from model import db, all_monitoring_items_detail
from config import DevConfig
from flask import Flask, request, jsonify
import time,datetime,json,requests
from config import DevConfig
from flask_cors import CORS, cross_origin

c20_template_for_frontend = Blueprint("c20_template_for_frontend", __name__)

# **********************************************************************
@c20_template_for_frontend.route("/c40_which_country_and_isp_are_impacted")
@c20_template_for_frontend.route("/c40_which_country_and_isp_are_impacted/")
def c40_which_country_and_isp_are_impacted():

    list_country=[]
    list_isp=[]
    dict_return_to_frontend={}
    all_the_row_that_have_impact = all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold == 2, all_monitoring_items_detail.paused_or_started != 3).all()
    for each_row in all_the_row_that_have_impact:
        country_name=each_row.group_name
        if country_name not in list_country:
            list_country.append(country_name)
        infra_that_is_impacted=each_row.belong_to_which_infra
        if infra_that_is_impacted not in list_isp and "not" not in infra_that_is_impacted :
            list_isp.append(infra_that_is_impacted)
    # print(f"list_country={list_country} / list_isp={list_isp}")
    dict_return_to_frontend["country_that_are_impact"]=list_country
    dict_return_to_frontend["isp_that_are_impact"]=list_isp
    print(f"dict_return_to_frontend={dict_return_to_frontend}")
    # list_all_the_data_in_all_monitoring_items_detail_table = [data.serialize_which_country_and_infra_are_impacted for data in all_the_row_that_have_impact]
    # return jsonify(list_all_the_data_in_all_monitoring_items_detail_table)
    return jsonify(dict_return_to_frontend)



# **********************************************************************
@c20_template_for_frontend.route("/c30_get_current_time")
@c20_template_for_frontend.route("/c30_get_current_time/")
def c30_get_current_time():
    current_time = datetime.datetime.now()
    new_time = current_time + datetime.timedelta(hours=8)
    formatted_time = new_time.strftime("%Y-%m-%d %H:%M:%S")  
    return formatted_time


# **********************************************************************
@c20_template_for_frontend.route("/c50_current_time_add_10_mins")
@c20_template_for_frontend.route("/c50_current_time_add_10_mins/")
def c50_current_time_add_10_mins():
    current_time = datetime.datetime.now()
    new_time = current_time + datetime.timedelta(hours=8,minutes=10)
    formatted_time = new_time.strftime("%Y-%m-%d %H:%M:%S")  
    return formatted_time
