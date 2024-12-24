from celery import shared_task
import flask_excel
from flask import render_template
import sqlite3
from models import Campaigns, Sponsor, Adrequests
from datetime import datetime
import logging
from mail_service import send_email
from jinja2 import Template, Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('.'))

def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)

def fetch_data(query):
    conn = sqlite3.connect('instance/IESCP_V2.sqlite3')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


@shared_task(ignore_result=False)
def create_csv(sponsor_id):
    resource = Campaigns.query.filter_by(sponsor_id=sponsor_id).all()
    
    if not resource:
        print("No campaigns found for the specified sponsor.")
        return None

    sponsor = Sponsor.query.filter_by(id=sponsor_id).first()
    if not sponsor:
        print(f"No sponsor found with id: {sponsor_id}.")
        return None

    print(f"Fetched sponsor username: {sponsor.username}")
    
    sponsor_name = sponsor.username.replace(" ", "_")
    task_id = create_csv.request.id  
    filename = f'{sponsor_name}_campaign_data_{task_id}.csv'

    print(f"Constructed filename: {filename}")

    column_names = [column.name for column in Campaigns.__table__.columns]
    try:
        csv_out = flask_excel.make_response_from_query_sets(resource, column_names=column_names, file_type='csv')
    except Exception as e:
        print(f"Error generating CSV response: {e}")
        return None

    if csv_out.data is None:
        print("CSV data is None. Cannot write to file.")
        return None
    
    try:
        with open(f'./instance/{filename}', 'wb') as file:
            file.write(csv_out.data)
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return None

    return filename

@shared_task(ignore_result=True)
def daily_reminder():
    query = """
    SELECT email FROM user
    WHERE login_count IS NULL OR last_login_at < DATETIME('now', '-1 day')
    """
    data = fetch_data(query)
    for row in data:
        email = row[0]
        if email == "admin@gmail.com":
            continue
        
        subject = "Reminder, please visit IESCP app."
        report_content = {
            "email": email
        }
        content_body = render_template("daily_reminder.html", report_content)
        send_email(email, subject, content_body)


@shared_task(ignore_result=True)
def adrequest_notification():
    query = """
    SELECT influencer.email, adrequests.messages, adrequests.requirements, adrequests.payment_amt, campaigns.name 
    FROM influencer 
    JOIN adrequests ON influencer.id = adrequests.influencer_id 
    JOIN campaigns ON adrequests.campaign_id = campaigns.id 
    WHERE adrequests.status = 'Pending'
    """
    data = fetch_data(query)  
    for row in data:
        email = row[0]
        ad_request_message = row[1]
        ad_requirements = row[2]
        ad_payment_amt = row[3]
        campaign_name = row[4]
        
        subject = "Reminder: You have a pending ad request"
        report_content = {
            "ad_request_msg": ad_request_message,
            "ad_req": ad_requirements,
            "ad_payment": ad_payment_amt,
            "campaign_name": campaign_name,
        }
        content_body = render_template("adrequest_notification.html", report_content)
        send_email(email, subject, content_body)



@shared_task(ignore_result=True)
def send_monthly_report():
    sponsors = Sponsor.query.all()
    
    for sponsor in sponsors:
        campaigns = Campaigns.query.filter_by(sponsor_id=sponsor.id).all()
        campaign_ids = [campaign.id for campaign in campaigns]
        
        adrequests = Adrequests.query.filter(Adrequests.campaign_id.in_(campaign_ids)).all()
        
        total_ads = len(adrequests)
        total_budget_used = sum(campaign.campaign_budget for campaign in campaigns)
        total_budget_remaining = float(sponsor.company_budget) - total_budget_used

        report_content = {
            "sponsor_name": sponsor.company_name,
            "total_ads": total_ads,
            "budget_used": total_budget_used,
            "budget_remaining": total_budget_remaining,
            "current_date": datetime.utcnow().strftime('%Y-%m-%d')
        }
        
        subject = "Monthly Report - IESCP"
        content_body = render_template("monthly_report.html", report_content)
        
        send_email(sponsor.email, subject, content_body)





