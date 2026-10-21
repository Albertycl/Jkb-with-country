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


axios_for_frontend = Blueprint("axios_for_frontend", __name__)




# **********************************************************************
@axios_for_frontend.route("/axios_query_db_all_monitoring_items_detail")
@axios_for_frontend.route("/axios_query_db_all_monitoring_items_detail/")
def axios_query_db_all_monitoring_items_detail():
    # paused_or_started==3 means paused
    # two_means_hit_threshold==2 means the alert is triggered
    list_all_the_data_in_all_monitoring_items_detail_table = all_monitoring_items_detail.query.filter(all_monitoring_items_detail.paused_or_started != 3,all_monitoring_items_detail.two_means_hit_threshold==2).order_by(all_monitoring_items_detail.two_means_hit_threshold.desc()).all()
    list_all_the_data_in_all_monitoring_items_detail_table = [data.serialize for data in list_all_the_data_in_all_monitoring_items_detail_table]
    return jsonify(list_all_the_data_in_all_monitoring_items_detail_table)

# **********************************************************************
@axios_for_frontend.route("/get_db_info_for_cdn_service_portal")
@axios_for_frontend.route("/get_db_info_for_cdn_service_portal/")
def get_db_info_for_cdn_service_portal():
    list_jkb_all_items=all_monitoring_items_detail.query.all()
    list_jkb_all_items = [data.serialize for data in list_jkb_all_items]
    return jsonify(list_jkb_all_items)



# **********************************************************************
@axios_for_frontend.route("/for_gary_handover_check_if_any_alert")
@axios_for_frontend.route("/for_gary_handover_check_if_any_alert/")
def for_gary_handover_check_if_any_alert():
    list_jkb_all_items=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.paused_or_started==1).all()
    list_jkb_all_items = [data.serialize for data in list_jkb_all_items]
    return str(len(list_jkb_all_items))



# **********************************************************************
@axios_for_frontend.route("/axios_get_country_list")
@axios_for_frontend.route("/axios_get_country_list/")
def axios_get_country_list():
    # paused_or_started==3 means paused
    # two_means_hit_threshold==2 means the alert is triggered
    # list_country = set([])
    # list_all_the_data_in_all_monitoring_items_detail_table = all_monitoring_items_detail.query.all()
    # for each_row in list_all_the_data_in_all_monitoring_items_detail_table:
    #     # print(f"each_row={each_row}")
    #     if "ignore" not in each_row.group_name:
    #         list_country.add(each_row.group_name)
    # try:
    #     list_country.remove("unclassified")
    #     list_country.remove("South_Asia")
    #     list_country.remove("North_Asia")
    #     list_country.remove("Brazil")
    # except Exception as error:
    #     print(f"error={error}")
    # str_list_country=','.join(list_country)
    # print(f"str_list_country={str_list_country}")
    str_list_country="China,Vietnam,Thailand,Indonesia,Korea,Cambodia"

    return jsonify(str_list_country)


# **********************************************************************
@axios_for_frontend.route("/axios_get_region_list")
@axios_for_frontend.route("/axios_get_region_list/")
def axios_get_region_list():
    str_list_country="North_Asia,South_Asia,Brazil"

    return jsonify(str_list_country)


# **********************************************************************
@axios_for_frontend.route("/all_the_monitor_items_for_this_country")
@axios_for_frontend.route("/all_the_monitor_items_for_this_country/<country_name>")
def all_the_monitor_items_for_this_country(country_name):
    all_the_rows_that_belong_in_this_country=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.group_name==country_name,~all_monitoring_items_detail.monitor_target_ip.contains("192.0.2.254"),~all_monitoring_items_detail.monitor_target_ip.contains("198.18.0.254"),~all_monitoring_items_detail.monitor_target_ip.contains("198.51.100.254"),~all_monitoring_items_detail.monitor_target_ip.contains("198.19.0.254")).order_by(all_monitoring_items_detail.two_means_hit_threshold.desc()).all()
    all_the_rows_that_belong_in_this_country = [data.serialize for data in all_the_rows_that_belong_in_this_country]
    return jsonify(all_the_rows_that_belong_in_this_country)



# **********************************************************************
def get_the_country_list():
    list_country = set([])
    list_all_the_data_in_all_monitoring_items_detail_table = all_monitoring_items_detail.query.all()
    for each_row in list_all_the_data_in_all_monitoring_items_detail_table:
        # print(f"each_row={each_row}")
        if "ignore" not in each_row.group_name:
            list_country.add(each_row.group_name)
    try:
        list_country.remove("unclassified")
    except Exception as error:
        print(f"error={error}")
    str_list_country=','.join(list_country)    
    return str_list_country

# **********************************************************************
@axios_for_frontend.route("/d60_count_how_many_alert_for_this_country_for_this_infra")
@axios_for_frontend.route("/d60_count_how_many_alert_for_this_country_for_this_infra/")
def d60_count_how_many_alert_for_this_country_for_this_infra():
    return_this_list=[]
    list_infra=["bravo","alpha"]
    
    # Bravo
    # 203.0.113.254 >only advertise to PCCW
    # 198.18.1.254->only advertise to TWG-Global
    # 198.19.0.254->only advertise to Sintel


    # Alpha
    # 192.0.2.254-> only advertise to TWG_Global
    # 198.18.0.254-> only advertise to Chief
    # 198.51.100.254-> only advertise to PCCW

    list_country_list=get_the_country_list().split(",")
    for each_country in list_country_list:
        for which_infra in list_infra:
            # ~all_monitoring_items_detail.monitor_target_ip.contains("192.0.2.254"),~all_monitoring_items_detail.monitor_target_ip.contains("198.18.0.254"),~all_monitoring_items_detail.monitor_target_ip.contains("198.51.100.254"),~all_monitoring_items_detail.monitor_target_ip.contains("198.19.0.254")
            # this part is removing the specific isp monitoring items, so that when isp has issue, it won't show up on the infra block and country block at the same time
            which_isp=""
            dict_key_country_name_value_number_of_alerts={}
            how_many_all_the_alert_under_this_infra_and_country=len(all_monitoring_items_detail.query.filter(all_monitoring_items_detail.group_name==each_country,all_monitoring_items_detail.belong_to_which_infra==which_infra,all_monitoring_items_detail.two_means_hit_threshold=="2",\
            ~all_monitoring_items_detail.monitor_target_ip.contains("192.0.2.254"),\
            ~all_monitoring_items_detail.monitor_target_ip.contains("198.18.0.254"),\
            ~all_monitoring_items_detail.monitor_target_ip.contains("198.51.100.254"),\
            ~all_monitoring_items_detail.monitor_target_ip.contains("203.0.113.254"),\
            ~all_monitoring_items_detail.monitor_target_ip.contains("198.18.1.254"),\
            ~all_monitoring_items_detail.monitor_target_ip.contains("198.19.0.254"),\
            ).all())
            if which_infra=="alpha":
                whole_row_when_country_and_infra_matches_infra_alpha=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.belong_to_which_infra==which_infra,all_monitoring_items_detail.group_name==each_country).first()
                if whole_row_when_country_and_infra_matches_infra_alpha!=None:
                    which_isp=whole_row_when_country_and_infra_matches_infra_alpha.alpha_isp

            elif which_infra=="bravo":
                whole_row_when_country_and_infra_matches_infra_bravo=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.belong_to_which_infra==which_infra,all_monitoring_items_detail.group_name==each_country).first()
                if whole_row_when_country_and_infra_matches_infra_bravo!=None:
                    which_isp=whole_row_when_country_and_infra_matches_infra_bravo.bravo_isp                
            

            # since these don't have jkb sensor, so just initilize myself
            if each_country=="Thailand" and which_infra=="alpha":
                which_isp="TWG-G"
            if each_country=="Indonesia" and which_infra=="alpha":
                which_isp="PCCW"        
            if each_country=="Korea" and which_infra=="alpha":
                which_isp="PCCW"     
            if each_country=="Cambodia" and which_infra=="alpha":
                which_isp="PCCW"   
            if each_country=="Brazil" and which_infra=="alpha":
                which_isp="PCCW"                                                       



            # since which_isp is a string, so need to convert it to a list 
            if which_isp!=None:
                which_isp=which_isp.split("/")
            
            dict_key_country_name_value_number_of_alerts["which_country"]=each_country
            dict_key_country_name_value_number_of_alerts["which_infra"]=which_infra
            dict_key_country_name_value_number_of_alerts["how_many_alerts"]=how_many_all_the_alert_under_this_infra_and_country
            dict_key_country_name_value_number_of_alerts["which_isp"]=which_isp
            return_this_list.append(dict_key_country_name_value_number_of_alerts)
    return jsonify(return_this_list)











2
# **********************************************************************
@axios_for_frontend.route("/d80_get_incoming_sensor_monitoring")
@axios_for_frontend.route("/d80_get_incoming_sensor_monitoring/")
@axios_for_frontend.route("/d80_get_incoming_sensor_monitoring/<which_infra>/<which_isp>")
def d80_get_incoming_sensor_monitoring(which_infra="alpha",which_isp="pccw"):
    which_infra=which_infra.lower()
    which_isp=which_isp.lower()
    if which_infra=="alpha" and which_isp=="pccw":
        all_the_rows_all_monitoring_items_detail=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="198.51.100.254").all()
        all_the_rows_all_monitoring_items_detail = [data.serialize for data in all_the_rows_all_monitoring_items_detail]
        return jsonify(all_the_rows_all_monitoring_items_detail)
    elif which_infra=="alpha" and which_isp=="twg-g":
        all_the_rows_all_monitoring_items_detail=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="192.0.2.254").all()
        all_the_rows_all_monitoring_items_detail = [data.serialize for data in all_the_rows_all_monitoring_items_detail]
        return jsonify(all_the_rows_all_monitoring_items_detail)
    elif which_infra=="alpha" and which_isp=="chief":
        all_the_rows_all_monitoring_items_detail=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="198.18.0.254").all()
        all_the_rows_all_monitoring_items_detail = [data.serialize for data in all_the_rows_all_monitoring_items_detail]
        return jsonify(all_the_rows_all_monitoring_items_detail)
    elif which_infra=="bravo" and which_isp=="singtel":
        all_the_rows_all_monitoring_items_detail=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="198.19.0.254").all()
        all_the_rows_all_monitoring_items_detail = [data.serialize for data in all_the_rows_all_monitoring_items_detail]
        return jsonify(all_the_rows_all_monitoring_items_detail)
    elif which_infra=="bravo" and which_isp=="pccw":
        all_the_rows_all_monitoring_items_detail=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="203.0.113.254").all()
        all_the_rows_all_monitoring_items_detail = [data.serialize for data in all_the_rows_all_monitoring_items_detail]
        return jsonify(all_the_rows_all_monitoring_items_detail)        
    elif which_infra=="bravo" and which_isp=="twg-g":
        all_the_rows_all_monitoring_items_detail=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="198.18.1.254").all()
        all_the_rows_all_monitoring_items_detail = [data.serialize for data in all_the_rows_all_monitoring_items_detail]
        return jsonify(all_the_rows_all_monitoring_items_detail)             
    else:
        return []


# **********************************************************************
@axios_for_frontend.route("/d90_a100_monitoring_specific_isp")
@axios_for_frontend.route("/d90_a100_monitoring_specific_isp/")
def d90_a100_monitoring_specific_isp():
    return_this_list=[]
    list_for_all_infra_and_isp=["alpha_pccw","alpha_twg_global","alpha_chief","bravo_singtel","bravo_pccw","bravo_twg_global"]
    dict_key_country_name_value_number_of_alerts={}
    for each_infra_and_isp in list_for_all_infra_and_isp:
        if each_infra_and_isp=="alpha_pccw":
            how_many_all_the_alert_under_this_infra_and_country=len(all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="198.51.100.254",all_monitoring_items_detail.two_means_hit_threshold=="2").all())
            dict_key_country_name_value_number_of_alerts=assign_infra_isp_how_many_alerts_to_dict("alpha",how_many_all_the_alert_under_this_infra_and_country,"ALPHA_PCCW")
            print(f"dict_key_country_name_value_number_of_alerts={dict_key_country_name_value_number_of_alerts}")
            return_this_list.append(dict_key_country_name_value_number_of_alerts)
        elif each_infra_and_isp=="alpha_twg_global":
            how_many_all_the_alert_under_this_infra_and_country=len(all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="192.0.2.254",all_monitoring_items_detail.two_means_hit_threshold=="2").all())
            dict_key_country_name_value_number_of_alerts=assign_infra_isp_how_many_alerts_to_dict("alpha",how_many_all_the_alert_under_this_infra_and_country,"ALPHA_TWG-G")
            return_this_list.append(dict_key_country_name_value_number_of_alerts)
        elif each_infra_and_isp=="alpha_chief":
            how_many_all_the_alert_under_this_infra_and_country=len(all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="198.18.0.254",all_monitoring_items_detail.two_means_hit_threshold=="2").all())
            dict_key_country_name_value_number_of_alerts=assign_infra_isp_how_many_alerts_to_dict("alpha",how_many_all_the_alert_under_this_infra_and_country,"ALPHA_CHIEF")
            return_this_list.append(dict_key_country_name_value_number_of_alerts)   
        elif each_infra_and_isp=="bravo_singtel":
            how_many_all_the_alert_under_this_infra_and_country=len(all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="198.19.0.254",all_monitoring_items_detail.two_means_hit_threshold=="2").all())
            dict_key_country_name_value_number_of_alerts=assign_infra_isp_how_many_alerts_to_dict("bravo",how_many_all_the_alert_under_this_infra_and_country,"BRAVO_Singtel")
            return_this_list.append(dict_key_country_name_value_number_of_alerts)   
        elif each_infra_and_isp=="bravo_pccw":
            how_many_all_the_alert_under_this_infra_and_country=len(all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="203.0.113.254",all_monitoring_items_detail.two_means_hit_threshold=="2").all())
            dict_key_country_name_value_number_of_alerts=assign_infra_isp_how_many_alerts_to_dict("bravo",how_many_all_the_alert_under_this_infra_and_country,"BRAVO_PCCW")
            return_this_list.append(dict_key_country_name_value_number_of_alerts)      
        elif each_infra_and_isp=="bravo_twg_global":
            how_many_all_the_alert_under_this_infra_and_country=len(all_monitoring_items_detail.query.filter(all_monitoring_items_detail.two_means_hit_threshold==2,all_monitoring_items_detail.monitor_target_ip=="198.18.1.254",all_monitoring_items_detail.two_means_hit_threshold=="2").all())
            dict_key_country_name_value_number_of_alerts=assign_infra_isp_how_many_alerts_to_dict("bravo",how_many_all_the_alert_under_this_infra_and_country,"BRAVO_TWG-G")
            return_this_list.append(dict_key_country_name_value_number_of_alerts)                                              
    return jsonify(return_this_list)



def assign_infra_isp_how_many_alerts_to_dict(which_infra,how_many_all_the_alert_under_this_infra_and_country,which_isp):
    dict_key_country_name_value_number_of_alerts={}
    dict_key_country_name_value_number_of_alerts["which_infra"]=which_infra
    dict_key_country_name_value_number_of_alerts["how_many_alerts"]=how_many_all_the_alert_under_this_infra_and_country
    dict_key_country_name_value_number_of_alerts["which_isp"]=which_isp
    return dict_key_country_name_value_number_of_alerts




# **********************************************************************
@axios_for_frontend.route("/get_one_time_child20_bottom_original_jkb_alert_table")
@axios_for_frontend.route("/get_one_time_child20_bottom_original_jkb_alert_table/")
def get_one_time_child20_bottom_original_jkb_alert_table():
    last_check_time_readable=str(all_monitoring_items_detail.query.first().last_check_time_readable)
    return last_check_time_readable