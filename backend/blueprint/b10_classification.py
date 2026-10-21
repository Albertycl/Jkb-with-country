# from flask import Flask
from model import db, all_monitoring_items_detail,monitor_group,cedexis_openmix,cedexis_platform
# from flask import Flask
from flask_migrate import Migrate
from config import DevConfig
from flask import Flask, request,jsonify,Blueprint
import requests,datetime,json,time,json,ipaddress,socket
from config import DevConfig
from flask_cors import CORS
from datetime import timedelta

b10_classification = Blueprint("b10_classification", __name__)




# # ******************************************************************
@b10_classification.route("/b20_get_the_group_list_for_probes")
@b10_classification.route("/b20_get_the_group_list_for_probes/")
def b20_get_the_group_list_for_probes():  
    db.session.query(monitor_group).delete()
    db.session.commit()    

    str_jkb_token = requests.get(f"http://127.0.0.1:5065/jkb_api_request_token_new_version").text
    headers = {'token': str(str_jkb_token)}
    url_for_the_list=["https://v6-api.jiankongbao.com/siteapi/monitor/group/list","https://v6-api.jiankongbao.com/siteapi/agent/group/list/"]
    for index,each_url in enumerate(url_for_the_list):
        dict_group_for_which_the_monitor_sensors_belong = requests.get(each_url, headers=headers).json()    
        list_all_the_id_for_jkb_agent=dict_group_for_which_the_monitor_sensors_belong["data"]
        for each_agent in list_all_the_id_for_jkb_agent:
            group_id=each_agent["group_id"]
            group_name=each_agent["group_name"]
            print(f"group_id={group_id} / group_name={group_name}")
            if "JP" not in group_name and "TEST ONLY" not in group_name:
                whole_row_to_insert=monitor_group(group_id=group_id,group_name=group_name)
                db.session.add(whole_row_to_insert)
                db.session.commit()
    
    for_all_rows_in_monitor_group=monitor_group.query.all()
    for each_row in for_all_rows_in_monitor_group:
        group_name=each_row.group_name
        print(f"group_name={group_name}")
        if "China" in group_name or "CM" in group_name or "CT" in group_name or "CU" in group_name or "CN_Probe" in group_name  :
            each_row.convert_to_the_name_i_want_to_show_in_frontend="China"
            db.session.commit()
        elif "_Probe" in group_name or "_Prob" in group_name:
            # after_replace_group_name=group_name.replace("_Prob","").replace("_Prob","")
            after_replace_group_name=group_name.split("_Prob")[0].split("_Probe")[0]
            each_row.convert_to_the_name_i_want_to_show_in_frontend=after_replace_group_name
            db.session.commit()
        elif "CN" in group_name:
            each_row.convert_to_the_name_i_want_to_show_in_frontend="China"
            db.session.commit()
        elif "South_East_Asia" in group_name and  "ID" in group_name:
            each_row.convert_to_the_name_i_want_to_show_in_frontend="INDO"
            db.session.commit()   
        elif "South_East_Asia" in group_name and "VN" in group_name:
            each_row.convert_to_the_name_i_want_to_show_in_frontend="VN"
            db.session.commit()     
        elif "South_East_Asia" in group_name and "TH" in group_name:
            each_row.convert_to_the_name_i_want_to_show_in_frontend="TH"
            db.session.commit()        
        elif "South_East_Asia_Redirect" in group_name:
            each_row.convert_to_the_name_i_want_to_show_in_frontend="------------ignore-----------"
            db.session.commit()      


    for each_row in for_all_rows_in_monitor_group:
        convert_to_the_name_i_want_to_show_in_frontend=each_row.convert_to_the_name_i_want_to_show_in_frontend    
        if convert_to_the_name_i_want_to_show_in_frontend=="KH":
            each_row.convert_to_the_name_i_want_to_show_in_frontend="Cambodia"
            db.session.commit()
        elif convert_to_the_name_i_want_to_show_in_frontend=="KR":
            each_row.convert_to_the_name_i_want_to_show_in_frontend="Korea"
            db.session.commit()            
        elif convert_to_the_name_i_want_to_show_in_frontend=="TH":
            each_row.convert_to_the_name_i_want_to_show_in_frontend="Thailand"
            db.session.commit()                        
        elif convert_to_the_name_i_want_to_show_in_frontend=="VN":
            each_row.convert_to_the_name_i_want_to_show_in_frontend="Vietnam"
            db.session.commit()                                    
        elif convert_to_the_name_i_want_to_show_in_frontend=="INDO":
            each_row.convert_to_the_name_i_want_to_show_in_frontend="Indonesia"
            db.session.commit()    

    b30_update_group_in_table_all_monitoring_items_detail()  
    b40_convert_the_monitor_target_domain_name_in_table_all_monitoring_items_detail_to_ip()     
    b41_check_if_unclassified_are_cdn_domains()
    b50_convert_the_ip_to_infra()                                                

    return "1"


# # ******************************************************************
@b10_classification.route("/b30_update_group_in_table_all_monitoring_items_detail")
@b10_classification.route("/b30_update_group_in_table_all_monitoring_items_detail/")
def b30_update_group_in_table_all_monitoring_items_detail():

    all_the_row_in_all_monitoring_items_detail=all_monitoring_items_detail.query.all()
    if all_the_row_in_all_monitoring_items_detail==[]:
        b20_get_the_group_list_for_probes()
    else:
        for each_row in all_the_row_in_all_monitoring_items_detail:
            group_id=each_row.group_id
            task_name=each_row.task_name
            whole_row_when_group_id_matches=monitor_group.query.filter(monitor_group.group_id==group_id).first()
            if whole_row_when_group_id_matches!=None:
                group_name=monitor_group.query.filter(monitor_group.group_id==group_id).first().convert_to_the_name_i_want_to_show_in_frontend
                each_row.group_name=group_name
                db.session.commit()
            else:
                if "(TH Domain)" in task_name:
                    each_row.group_name="Thailand"
                    db.session.commit()
                elif "(BZ)" in task_name:
                    each_row.group_name="Brazil"
                    db.session.commit()    
                elif "(TH)" in task_name:
                    each_row.group_name="Thailand"
                    db.session.commit()      
                elif "(ID)" in task_name:
                    each_row.group_name="Indonesia"
                    db.session.commit()      
                else:
                    each_row.group_name="unclassified"
                    db.session.commit()                      

    # b40_convert_the_monitor_target_domain_name_in_table_all_monitoring_items_detail_to_ip()     
    # b50_convert_the_ip_to_infra()                                                

    return "1"
                                                
      

# # ******************************************************************
# @b10_classification.route("/b40_convert_the_monitor_target_domain_name_in_table_all_monitoring_items_detail_to_ip")
# @b10_classification.route("/b40_convert_the_monitor_target_domain_name_in_table_all_monitoring_items_detail_to_ip/")
def b40_convert_the_monitor_target_domain_name_in_table_all_monitoring_items_detail_to_ip():    
    all_the_rows_in_table_all_monitoring_items_detail=all_monitoring_items_detail.query.all()  
    for each_row in all_the_rows_in_table_all_monitoring_items_detail:
        monitor_target=each_row.monitor_target
        try:
            ip=ipaddress.ip_address(monitor_target)
            each_row.monitor_target_ip=ip
            db.session.commit()
        except Exception as error:
            try:
                ip = socket.gethostbyname(monitor_target)
                
                # print(f"monitor_target={monitor_target} / ip={ip}")
                each_row.monitor_target_ip=ip
                db.session.commit()
            except Exception as error:
                # print(f"monitor_target={monitor_target} / error={error}")
                each_row.monitor_target_ip="check_by_yourself"
                db.session.commit()

    return "1"



# # ******************************************************************
@b10_classification.route("/b41_check_if_unclassified_are_cdn_domains")
@b10_classification.route("/b41_check_if_unclassified_are_cdn_domains/")
def b41_check_if_unclassified_are_cdn_domains():   
    all_row_that_are_unclassififed=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.belong_to_which_infra=="Target host does not find on the DB").all()
    for each_unclassififed_row in all_row_that_are_unclassififed:
        monitor_target=each_unclassififed_row.monitor_target
        print(f"monitor_target={monitor_target}")
        row_if_monitor_target_is_cdn_domain=cedexis_openmix.query.filter(cedexis_openmix.cdn_domain==monitor_target).first()
        print(f"monitor_target={monitor_target} / row_if_monitor_target_is_cdn_domain={row_if_monitor_target_is_cdn_domain}")
        if row_if_monitor_target_is_cdn_domain!=None:
            each_unclassififed_row.belong_to_which_infra="CDX_Openmix"
            db.session.commit()

        else:
            whole_row_when_contains_match=cedexis_platform.query.filter(cedexis_platform.primeSecureUrl.contains(monitor_target)).first()
            if whole_row_when_contains_match!=None:
                name=whole_row_when_contains_match.name
                each_unclassififed_row.belong_to_which_infra="CDX_Platform"
                db.session.commit()

    return "1"


# # ******************************************************************
# @b10_classification.route("/b45_convert_single_monitor_to_ip")
# @b10_classification.route("/b45_convert_single_monitor_to_ip/")
def b45_convert_single_monitor_to_ip(row_id):    
    the_row_when_the_row_id_matches=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.id==row_id).first()  
    monitor_target=the_row_when_the_row_id_matches.monitor_target
    try:
        ip=ipaddress.ip_address(monitor_target)
        the_row_when_the_row_id_matches.monitor_target_ip=ip
        db.session.commit()
    except Exception as error:
        try:
            ip = socket.gethostbyname(monitor_target)
            
            # print(f"monitor_target={monitor_target} / ip={ip}")
            the_row_when_the_row_id_matches.monitor_target_ip=ip
            db.session.commit()
        except Exception as error:
            the_row_when_the_row_id_matches.monitor_target_ip="check_by_yourself"
            db.session.commit()

    b55_convert_single_ip_to_infra(row_id)
    return "1"

                          


# # ******************************************************************
@b10_classification.route("/b50_convert_the_ip_to_infra")
@b10_classification.route("/b50_convert_the_ip_to_infra/")
def b50_convert_the_ip_to_infra():  
    all_rows_all_monitoring_items_detail=all_monitoring_items_detail.query.all()
    for each_row in all_rows_all_monitoring_items_detail:
       monitor_target_ip=each_row.monitor_target_ip
       print(f"monitor_target_ip={monitor_target_ip}")
       try:
            belong_to_which_infra = requests.get(f"{DevConfig.INFRA_LOOKUP_URL}/api/queryhost/{monitor_target_ip}").json()["details"]
            each_row.belong_to_which_infra=belong_to_which_infra
            db.session.commit()
       except Exception as error:  
           print(f"in route b50_convert_the_ip_to_infra / error = {error}")

    all_monitoring_items_detail.query.all()

    return "1"



# # ******************************************************************
@b10_classification.route("/b55_convert_single_ip_to_infra")
@b10_classification.route("/b55_convert_single_ip_to_infra/")
def b55_convert_single_ip_to_infra(row_id):  
    the_row_when_the_row_id_matches=all_monitoring_items_detail.query.filter(all_monitoring_items_detail.id==row_id).first()
    monitor_target_ip=the_row_when_the_row_id_matches.monitor_target_ip
    belong_to_which_infra = requests.get(f"{DevConfig.INFRA_LOOKUP_URL}/api/queryhost/{monitor_target_ip}").json()["details"]
    the_row_when_the_row_id_matches.belong_to_which_infra=belong_to_which_infra
    db.session.commit()
    return "1"
