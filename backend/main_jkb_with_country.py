import requests,json
#########Migrations#############
from flask import Flask,render_template,Blueprint,request,abort
from blueprint.a10_all_jkb_sensor_status import a10_all_jkb_sensor_status
# from blueprint.axios_for_service_portal_cdn_information import axios_for_service_portal_cdn_information
from blueprint.axios_for_frontend import axios_for_frontend
from blueprint.ct_cu_cm_count_how_many_not_availiable import ct_cu_cm_count_how_many_not_availiable
from blueprint.c20_template_for_frontend import c20_template_for_frontend
from blueprint.b10_classification import b10_classification
from blueprint.c10_cedexis import c10_cedexis
from blueprint.a20_alert_threshold import a20_alert_threshold
from blueprint.e10_udpate_isp_for_which_country import e10_udpate_isp_for_which_country



#########Migrations#############
from model import db
from flask_cors import CORS
from flask_migrate import Migrate
app = Flask(__name__)

app.register_blueprint(a10_all_jkb_sensor_status)
# app.register_blueprint(axios_for_service_portal_cdn_information)
app.register_blueprint(axios_for_frontend)
app.register_blueprint(ct_cu_cm_count_how_many_not_availiable)
app.register_blueprint(c20_template_for_frontend)
app.register_blueprint(b10_classification)
app.register_blueprint(c10_cedexis)
app.register_blueprint(a20_alert_threshold)
app.register_blueprint(e10_udpate_isp_for_which_country)

migrate = Migrate(app, db)
from config import DevConfig
app.config.from_object(DevConfig)
db.init_app(app)
CORS(app)

# Routes that call the JianKongBao/Cedexis/infra APIs or rewrite the tables.
# They stay off unless ENABLE_POLLERS=true (the demo runs on seeded data).
POLLER_PREFIXES = (
    "/jkb_api_request_token_new_version", "/a10_", "/a20_", "/a30_",
    "/b20_", "/b30_", "/b41_", "/b50_", "/b55_", "/c20_getting_cedexis_data",
    "/c30_get_platform", "/e11_", "/get_alert_threshold",
)


@app.before_request
def block_pollers_when_disabled():
    if not DevConfig.ENABLE_POLLERS and request.path.startswith(POLLER_PREFIXES):
        abort(403, description="Poller endpoints are disabled (ENABLE_POLLERS=false)")


# this is for getting the token
@app.route('/jkb_api_request_token_new_version')
def jkb_api_request_token_new_version():
    response_code_from_api = requests.get(
        "https://v6-api.jiankongbao.com/userapi/common/apitoken",
        params={
            "user_email": DevConfig.JKB_USER_EMAIL,
            "user_pwd": DevConfig.JKB_USER_PWD,
            "client_id": DevConfig.JKB_CLIENT_ID,
            "client_secret": DevConfig.JKB_CLIENT_SECRET,
        },
    )
    dic_from_response = json.loads(response_code_from_api.text)
    return dic_from_response["token"]



# Add this function at the bottom of your Flask application code
def create_app(host='0.0.0.0', port=5065):
    app.run(host=host, port=int(port))
    return app