from flask import Flask, jsonify, request
from flask_security import Security
from flask_restful import Api
from flask_cors import CORS
from config import DevelopmentConfig
from models import db, user_datastore
from caching import cache
from celery_factory import celery_init_app
from task import create_csv, daily_reminder, adrequest_notification, send_monthly_report
import flask_excel as excel
from celery.schedules import crontab


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    cache.init_app(app)
    app.security = Security(app, user_datastore)
    CORS(app)
    with app.app_context():
        db.create_all()
        import routes.views
    return app, api, cache

app, api, cache = create_app()
celery_app = celery_init_app(app)

from routes.auth import *
api.add_resource(AdminLogin, '/admin/login')
api.add_resource(SponsorRegister, '/sponsor/register')
api.add_resource(SponsorLogin, '/sponsor/login')
api.add_resource(InfluencerRegister, '/influencer/register')
api.add_resource(InfluencerLogin, '/influencer/login')

from routes.admin import *
api.add_resource(SponsorApproval, '/admin/sponsor/<int:id>/approve')
api.add_resource(SponsorResources, '/sponsor_resources')
api.add_resource(SponsorFlagging, '/admin/sponsor/<int:id>/flagging')
api.add_resource(SponsorUnFlagging, '/admin/sponsor/<int:id>/unflagging')

api.add_resource(InfluencerResources, '/influencer_resources')
api.add_resource(InfluencerFlagging, '/admin/influencer/<int:id>/flagging')
api.add_resource(InfluencerUnFlagging, '/admin/influencer/<int:id>/unflagging')

api.add_resource(CampaignResources, '/campaign_resources')
api.add_resource(CampaignFlagging, '/admin/campaign/<int:id>/flagging')
api.add_resource(CampaignUnFlagging, '/admin/campaign/<int:id>/unflagging')

api.add_resource(AdminOverallStatistics, '/admin_overall_stats')


from routes.campaigns import *
api.add_resource(CampaignResource, '/sponsor/campaign')
api.add_resource(CampaignDetailResource,'/sponsor/campaign/<int:id>')
api.add_resource(CompanyBudgetResource, '/sponsor/company_budget')

api.add_resource(SponsorReceivedAdRequestResource, 
                 '/sponsor/ad_requests/<int:sponsor_id>', 
                 endpoint='get_ad_requests_for_sponsor', 
                 methods=['GET'])  # For fetching ad requests sent by influencers to a sponsor's campaigns

api.add_resource(SponsorReceivedAdRequestResource, 
                 '/sponsor/ad_requests/<int:adrequest_id>', 
                 endpoint='update_sponsor_ad_request_status', 
                 methods=['PUT'])  # For accepting/rejecting a specific ad request by sponsor

api.add_resource(GetSponsorDetails, '/sponsor/details/<int:sponsor_id>') # to get sponsor_details

api.add_resource(CampaignSearchResource, '/search/campaigns') # influencer searching campaings
api.add_resource(SponsorStatistics, '/sponsor/<int:sponsor_id>/statistics') # sponsor stats
api.add_resource(Create_csv, '/export_csv') # generating the report
api.add_resource(GetCSV, '/get-csv/<id>') # downloading the report


from routes.influencers import *
api.add_resource(ActiveInfluencers, '/all_active/influencers') # retrieve all active infleuncer and show to sponsor
api.add_resource(PublicCampaigns, '/all_public_campaigns') # retrieve all public campaigns and show to influencer
api.add_resource(SubmitInfluencerAdRequest, '/influencer/ad_request') # influencer sending a adrequest to sponsor
api.add_resource(InfluencerAdRequestResource, '/influencer/ad_request/<int:influencer_id>')
api.add_resource(InfluencerAdRequestSpecificResource, '/influencer_specific_ad_request/<int:adrequest_id>')

api.add_resource(InfluencerReceivedAdRequestResource, 
                 '/influencer/ad_requests/<int:influencer_id>', 
                 endpoint='get_ad_requests_for_influencer', 
                 methods=['GET']) # For fetching ad requests for an influencer

api.add_resource(InfluencerReceivedAdRequestResource, 
                 '/influencer/ad_requests/<int:adrequest_id>', 
                 endpoint='update_ad_request_status', 
                 methods=['PUT']) # For accepting/rejecting a specific ad request

api.add_resource(UpdateInfluencerDetails, '/influencer/update_details/<int:influencer_id>') # influencer updating profile
api.add_resource(GetInfluencerDetails, '/influencer/profile/<int:influencer_id>') # to fetch influencer details
api.add_resource(InfluencerResource, '/search/influencers') # sponsor search for influencer
api.add_resource(InfluencerStatistics, '/influencer/<int:influencer_id>/statistics') # influencer stats



from routes.adrequests import *
api.add_resource(AdRequestResource, '/sponsor/ad_request') # to create an adrequest
api.add_resource(SponsorAdRequestResource, '/sponsor/ad_request/<int:sponsor_id>')
api.add_resource(AdrequestSpecificResource, '/ad_request/<int:adrequest_id>')

excel.init_excel(app)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=55),
        daily_reminder.s(),
    )
    
    sender.add_periodic_task(
        crontab(hour=19, minute=55),
        adrequest_notification.s(),
    )

    sender.add_periodic_task(
        crontab(hour=19, minute=55, day_of_month=25),
        send_monthly_report.s(),
    )



if __name__ == "__main__":
    app.run(debug = True)
