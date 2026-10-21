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

c10_cedexis = Blueprint("c10_cedexis", __name__)


# # ******************************************************************
@c10_cedexis.route("/c20_getting_cedexis_data")
@c10_cedexis.route("/c20_getting_cedexis_data") 
def c20_getting_cedexis_data():
    db.session.query(cedexis_openmix).delete()
    db.session.commit()    
    
    headers = {'Authorization': f'Bearer {DevConfig.CEDEXIS_TOKEN}'}
    list_response = requests.get(f'https://portal.cedexis.com:443/api/v2/config/applications/dns.json/', headers=headers).json()
    # str_list_response=json.dumps(list_response)
    # with open('data.json', 'a') as file:
    # # write the JSON string to the file
    #     file.write(str_list_response)

    #     # close the file
    # file.close()  
    for dict_each_row in list_response:
        print(f"\n\n")
        id=dict_each_row["id"]
        cdn_domain=dict_each_row["name"].replace("_RTT","")
        list_platforms=dict_each_row["platforms"]
        for each_row in list_platforms:
            cname=each_row["cname"]
            try:
                china_handicap=each_row["geo"]["country"]["CN"]["handicap"]
                china_enabled=each_row["geo"]["country"]["CN"]["enabled"]
                global_handicap=each_row["geo"]["global"]["handicap"]
                global_enabled=each_row["geo"]["global"]["enabled"]
                print(f"cdn_domain={cdn_domain} / cname={cname} /  global_enabled={global_enabled}")
                whole_row_to_insert=cedexis_openmix(cdn_domain=cdn_domain,cname=cname,global_enabled=global_enabled)
                db.session.add(whole_row_to_insert)
                db.session.commit()
            except Exception as error:
                print(f"cdn_domain={cdn_domain} / error={error}")
   
    return "1"


# # ******************************************************************
@c10_cedexis.route("/c30_get_platform")
@c10_cedexis.route("/c30_get_platform") 
def c30_get_platform():
    # db.session.query(cedexis).delete()
    # db.session.commit()    
    with open("data.json", "w") as file:
        file.write("") #empty the file
    headers = {'Authorization': f'Bearer {DevConfig.CEDEXIS_TOKEN}'}
    list_response = requests.get(f'https://portal.cedexis.com:443/api/v2/config/platforms.json', headers=headers).json()
    for each_row in list_response:
        name="cdx_platform_"+each_row["name"]
        displayName=each_row["displayName"]
        primeSecureUrl=each_row["radarConfig"]["primeSecureUrl"]
        print(f"name={name} / primeSecureUrl={primeSecureUrl}")
        whole_row_to_insert = cedexis_platform(name=name,primeSecureUrl=primeSecureUrl)
        db.session.add(whole_row_to_insert)
        db.session.commit()
    # str_list_response=json.dumps(list_response)
    # with open('data.json', 'a') as file:
    # # write the JSON string to the file
    #     file.write(str_list_response)

    #     # close the file
    # file.close()

    return "1"