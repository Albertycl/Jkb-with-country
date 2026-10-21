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

e10_udpate_isp_for_which_country = Blueprint("e10_udpate_isp_for_which_country", __name__)


# ******************************************************************
@e10_udpate_isp_for_which_country.route("/e11_update_the_isp_for_this_country")
@e10_udpate_isp_for_which_country.route("/e11_update_the_isp_for_this_country/") 
def e11_update_the_isp_for_this_country():
    # create new row for cambodia alpha / korea alpha indonesia alpha / thailand alpha / brazil alpha
    # all_the_countries_that_need_to_add=["Cambodia","Korea","Indonesia","Thailand","Brazil"]
    # for each_country in all_the_countries_that_need_to_add:
    #     whole_row_to_insert=all_monitoring_items_detail(group_name=each_country,belong_to_which_infra="ALPHA")
    #     db.session.add(whole_row_to_insert)

        
    all_the_rows=all_monitoring_items_detail.query.all()
    for each_row in all_the_rows:


        if each_row.group_name=="China" and each_row.belong_to_which_infra=="ALPHA":
            each_row.alpha_isp="CT/CU/CMI"
            db.session.commit() 
        elif each_row.group_name=="China" and each_row.belong_to_which_infra=="BRAVO":            
            each_row.bravo_isp="CT/CU/CMI/CN2"
            db.session.commit() 


        elif each_row.group_name=="Vietnam" and each_row.belong_to_which_infra=="ALPHA":
            each_row.alpha_isp="Chief-VNPT/PCCW"
            db.session.commit() 
        elif each_row.group_name=="Vietnam" and each_row.belong_to_which_infra=="BRAVO":            
            each_row.bravo_isp="TWG-G+Singtel-VNPT/TWG-G Viettel/PCCW"   
            db.session.commit()  


        elif each_row.group_name=="Thailand" and each_row.belong_to_which_infra=="ALPHA":
            each_row.alpha_isp="TWG-G"
            db.session.commit() 
        elif each_row.group_name=="Thailand" and each_row.belong_to_which_infra=="BRAVO":            
            each_row.bravo_isp="PCCW"
            db.session.commit() 


        elif each_row.group_name=="Indonesia" and each_row.belong_to_which_infra=="ALPHA":
            each_row.alpha_isp="TWG-G"
            db.session.commit() 
        elif each_row.group_name=="Indonesia" and each_row.belong_to_which_infra=="BRAVO":            
            each_row.bravo_isp="PCCW"
            db.session.commit()  


        elif each_row.group_name=="Cambodia" and each_row.belong_to_which_infra=="ALPHA":
            each_row.alpha_isp="TWG-G"
            db.session.commit() 
        elif each_row.group_name=="Cambodia" and each_row.belong_to_which_infra=="BRAVO":            
            each_row.bravo_isp="PCCW" 
            db.session.commit() 


        elif each_row.group_name=="Brazil" and each_row.belong_to_which_infra=="ALPHA":
            each_row.alpha_isp="PCCW"
            db.session.commit() 
        elif each_row.group_name=="Brazil" and each_row.belong_to_which_infra=="BRAVO":            
            each_row.bravo_isp="PCCW" 
            db.session.commit() 


        elif each_row.group_name=="Korea" and each_row.belong_to_which_infra=="ALPHA":
            each_row.alpha_isp="PCCW"
            db.session.commit() 
        elif each_row.group_name=="Korea" and each_row.belong_to_which_infra=="BRAVO":            
            each_row.bravo_isp="PCCW"
            db.session.commit() 

    return "1"
                                                        

            

        

   