
from sqlalchemy.dialects.postgresql import JSON
import datetime
# from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import TIMESTAMP
db = SQLAlchemy()


class all_monitoring_items_detail(db.Model):
    __tablename__ = "all_monitoring_items_detail"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255))
    task_name = db.Column(db.String(255))
    task_summary = db.Column(db.String(255))
    alert_threshold =  db.Column(db.String(255))
    threshold_as_a_list= db.Column(db.String(255))
    group_id = db.Column(db.String(255))
    task_type = db.Column(db.String(255))
    link_for_availability = db.Column(db.String(255))
    link_for_snapshot = db.Column(db.String(255))
    link_for_response_time = db.Column(db.String(255))
    # 3 is paused
    paused_or_started = db.Column(db.String(255))
    two_means_hit_threshold = db.Column(db.String(255))
    last_resp_status = db.Column(db.String(255))
    last_resp_time = db.Column(db.String(255))
    last_check_time = db.Column(db.String(255))
    monitor_target = db.Column(db.String(255))
    last_check_time_readable = db.Column(db.DateTime)
    how_many_ct_not_available = db.Column(db.String(255), default='default_none')
    how_many_cu_not_available = db.Column(db.String(255), default='default_none')
    how_many_cm_not_available = db.Column(db.String(255), default='default_none')
    how_many_other_isp_not_available = db.Column(db.String(255), default='default_none')
    group_name = db.Column(db.String(255))
    monitor_target_ip = db.Column(db.String(255))
    belong_to_which_infra = db.Column(db.String(255))
    link_for_edit_threshold= db.Column(db.String(255))
    alpha_isp= db.Column(db.String(255))
    bravo_isp= db.Column(db.String(255))
    
  

    @property
    def serialize(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_summary": self.task_summary,
            "group_id": self.group_id,
            "task_type": self.task_type,
            "link_for_availability": self.link_for_availability,
            "link_for_snapshot": self.link_for_snapshot,
            "link_for_response_time": self.link_for_response_time,
            "paused_or_started": self.paused_or_started,
            "two_means_hit_threshold": self.two_means_hit_threshold,
            "last_resp_status": self.last_resp_status,
            "last_resp_time": self.last_resp_time,
            "last_check_time": self.last_check_time,
            "last_check_time_readable": f"{self.last_check_time_readable}",
            "how_many_ct_not_available": self.how_many_ct_not_available,
            "how_many_cu_not_available": self.how_many_cu_not_available,
            "how_many_cm_not_available": self.how_many_cm_not_available,
            "how_many_other_isp_not_available": self.how_many_other_isp_not_available,
            "group_name":self.group_name,
            "monitor_target_ip":self.monitor_target_ip,
            "belong_to_which_infra":self.belong_to_which_infra,
            "alert_threshold":self.alert_threshold,
            "threshold_as_a_list":self.threshold_as_a_list,
            "alpha_isp":self.alpha_isp,
            "bravo_isp":self.bravo_isp,
        }


    @property
    def serialize_which_country_and_infra_are_impacted(self):
        return {
            "group_name":self.group_name,
            "belong_to_which_infra":self.belong_to_which_infra,
        }
    
    @property
    def serialize_for_threshold(self):
        return {
            "task_id":self.task_id,
            "task_name":self.task_name,
            "alert_threshold":self.alert_threshold,
            "link_for_snapshot": self.link_for_snapshot,
            "link_for_edit_threshold": self.link_for_edit_threshold,
        }



# ***************************************************************************************
class monitor_group(db.Model):
    __tablename__ = "monitor_group"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    group_name = db.Column(db.String(255))
    convert_to_the_name_i_want_to_show_in_frontend = db.Column(db.String(255))


    @property
    def serialize_for_threshold(self):
        return {
            "group_id":self.task_id,
            "group_name":self.group_name,
            "convert_to_the_name_i_want_to_show_in_frontend":self.convert_to_the_name_i_want_to_show_in_frontend,

        }




# ***************************************************************************************
class cedexis_openmix(db.Model):
    __tablename__ = "cedexis_openmix"
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(255))
    cdn_domain = db.Column(db.String(255))
    global_enabled = db.Column(db.String(255))


    



# ***************************************************************************************
class cedexis_platform(db.Model):
    __tablename__ = "cedexis_platform"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    primeSecureUrl = db.Column(db.String(255))
