from flask_restful import Resource
from flask import request, jsonify, make_response, send_file
from flask_security import auth_required, roles_accepted
from models import db, Campaigns, Adrequests, Influencer, Sponsor
from datetime import datetime, date
import os
from task import create_csv
from celery.result import AsyncResult

def get_company_budget(sponsor_id):
    # Assuming you have a Company or Sponsor model where the budget is stored
    sponsor = Sponsor.query.filter_by(id=sponsor_id).first()
    if not sponsor:
        raise ValueError("Sponsor not found")
    
    # Assuming `sponsor.company_budget` contains the company's budget
    return sponsor.company_budget




# Campaign creation and retrieval
class CampaignResource(Resource):
    @auth_required("token")
    @roles_accepted('admin', 'sponsor')
    def post(self):
        data = request.get_json()

        name = data.get('name')
        niche = data.get('niche')
        sponsor_id = data.get('sponsor_id')
        description = data.get('description')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        budget = data.get('budget')
        visibility = data.get('visibility')
        goals = data.get('goals')

        # Error handling for mandatory fields
        if not name or not description:
            return make_response(jsonify({"message": "name and description are required"}), 400)
        if not start_date_str or not end_date_str:
            return make_response(jsonify({"message": "start_date and end_date are required"}), 400)
        if budget is None:
            return make_response(jsonify({"message": "budget is required"}), 400)

        # Convert date strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return make_response(jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400)

        # Check if the end_date is in the past
        current_date = datetime.now().date()
        if end_date.date() <= current_date:
            return make_response(jsonify({"message": "The end date must be in the future."}), 400)

        # Get the sponsor's company budget from the database
        company_budget = Sponsor.query.get(sponsor_id).company_budget
        if int(budget) > int(company_budget):
            return make_response(jsonify({"message": f"Campaign budget exceeds the company budget ({company_budget})"}), 400)

        # Create and save the new campaign
        new_campaign = Campaigns(
            name=name,
            niche=niche,
            sponsor_id=sponsor_id,
            description=description,
            start_date=start_date,
            end_date=end_date,
            campaign_budget=budget,
            visibility=visibility,
            goals=goals,
        )
        db.session.add(new_campaign)
        db.session.commit()
        return make_response(jsonify({"message": "Campaign created successfully", "id": new_campaign.id}), 201)

    @auth_required("token")
    @roles_accepted('sponsor')
    def get(self):
        sponsor_id = request.headers.get('Sponsor-ID')
        if not sponsor_id:
            return make_response(jsonify({"message": "Sponsor ID not provided"}), 400)

        campaigns = Campaigns.query.filter_by(sponsor_id=sponsor_id).all()

        campaign_data = []
        for campaign in campaigns:
            campaign_info = {
                'id': campaign.id,
                'name': campaign.name,
                'niche': campaign.niche,
                'description': campaign.description,
                'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'budget': campaign.campaign_budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals,
                'flagged': campaign.flagged,
            }
            campaign_data.append(campaign_info)

        if not campaign_data:
            return make_response(jsonify({"message": "No campaigns found for this sponsor"}), 404)

        return make_response(jsonify({"message": "Campaigns retrieved successfully", "data": campaign_data}), 200)




class CompanyBudgetResource(Resource):
    @auth_required("token")
    @roles_accepted('sponsor')
    def get(self):
        sponsor_id = request.headers.get('Sponsor-ID')
        
        if not sponsor_id:
            return make_response(jsonify({"message": "Sponsor ID not provided"}), 400)
        
        # Fetch the sponsor and their company budget
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        
        company_budget = sponsor.company_budget

        return make_response(jsonify({"company_budget": company_budget}), 200)


# Class to handle single campaign actions (GET, PUT, DELETE)
class CampaignDetailResource(Resource):
    @auth_required("token")
    @roles_accepted('sponsor', 'admin')
    def get(self, id):
        campaign = Campaigns.query.filter_by(id=id).first()
        if not campaign:
            return make_response(jsonify({"message": "No campaign found"}), 404)

        campaign_info = {
            'id': campaign.id,
            'name': campaign.name,
            'niche': campaign.niche,
            'description': campaign.description,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'budget': campaign.campaign_budget,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'flagged': campaign.flagged,
            'sponsor_id': campaign.sponsor_id,
        }
        return make_response(jsonify({"message": "Campaign found", "data": campaign_info}), 200)

    @auth_required("token")
    @roles_accepted('sponsor', 'admin')
    def put(self, id):
        campaign = Campaigns.query.filter_by(id=id).first()
        if not campaign:
            return make_response(jsonify({"message": "No campaign found by that id"}), 404)

        data = request.get_json()

        if not data.get('name'):
            return make_response(jsonify({"message": "name is required"}), 400)

        try:
            sponsor_id = data['sponsor_id']
            company_budget = get_company_budget(sponsor_id)

            if int(data.get('budget')) > int(company_budget):
                return make_response(jsonify({"message": f"Campaign budget cannot exceed company budget of {company_budget}"}), 400)

            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()  # Convert to date
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()  # Convert to date
            current_date = date.today()  # Get today's date

            if end_date <= current_date:
                return make_response(jsonify({"message": "End date must be in the future."}), 400)

            if end_date < start_date:
                return make_response(jsonify({"message": "End date cannot be earlier than start date."}), 400)

            # Updating the campaign with valid data
            campaign.name = data['name']
            campaign.description = data['description']
            campaign.sponsor_id = data['sponsor_id']
            campaign.campaign_budget = data['budget']
            campaign.start_date = start_date  # Update with date object
            campaign.end_date = end_date      # Update with date object
            campaign.visibility = data.get('visibility')
            campaign.goals = data.get('goals')
            campaign.niche = data.get('niche')

            # # Debugging: log the campaign data
            # print("Campaign data to be updated:", {
            #     "name": campaign.name,
            #     "description": campaign.description,
            #     "sponsor_id": campaign.sponsor_id,
            #     "campaign_budget": campaign.campaign_budget,
            #     "start_date": campaign.start_date,
            #     "end_date": campaign.end_date,  # Log the updated end date
            #     "visibility": campaign.visibility,
            #     "goals": campaign.goals,
            #     "niche": campaign.niche,
            # })

            db.session.commit()  # Commit the changes
            return make_response(jsonify({"message": "Campaign updated successfully", "id": campaign.id}), 200)
        except Exception as e:
            db.session.rollback()
            print("Error during updating campaign:", str(e))  # Log any errors
            return make_response(jsonify({"message": "An error occurred: " + str(e)}), 500)

    @auth_required("token")
    @roles_accepted('admin', 'sponsor')
    def delete(self, id):
        campaign = Campaigns.query.filter_by(id=id).first()
        if not campaign:
            return make_response(jsonify({"message": "No campaign found"}), 404)
        ad_requests = Adrequests.query.filter_by(campaign_id=id).all()

        if ad_requests:
            for ad_request in ad_requests:
                db.session.delete(ad_request)
        db.session.delete(campaign)
        db.session.commit()
        return make_response(jsonify({"message": "Campaign and associated ad requests deleted successfully", "id": id}), 200)




class SponsorReceivedAdRequestResource(Resource):
    @auth_required("token")
    @roles_accepted('sponsor')
    def get(self, sponsor_id):
        # Fetch ad requests received by the sponsor's campaigns
        ad_requests = (
            db.session.query(
                Adrequests,
                Campaigns.name.label('campaign_name'),
                Campaigns.flagged.label('campaign_flagged'),  # Include flagged status for the campaign
                Influencer.username.label('influencer_name'),
                Influencer.reach.label('influencer_reach'),
                Influencer.niche.label('influencer_niche'),
                Influencer.platform.label('influencer_platform'),
                Influencer.flagged.label('influencer_flagged')
            )
            .join(Campaigns, Adrequests.campaign_id == Campaigns.id)
            .join(Influencer, Adrequests.influencer_id == Influencer.id)
            .filter(Campaigns.sponsor_id == sponsor_id, Adrequests.sent_by_sponsor.is_(False))
            .all()
        )

        if not ad_requests:
            return make_response(jsonify({"message": "No ad requests found for this sponsor."}), 404)

        data = []
        for ad_request, campaign_name, campaign_flagged, influencer_name, influencer_reach, influencer_niche, influencer_platform, influencer_flagged in ad_requests:
            ad_request_info = {
                'id': ad_request.id,
                'messages': ad_request.messages,
                'requirements': ad_request.requirements,
                'status': ad_request.status,
                'payment_amt': ad_request.payment_amt,
                'campaign_name': campaign_name,
                'campaign_flagged': campaign_flagged,  # Add campaign flagged status to the response
                'influencer_name': influencer_name,
                'influencer_reach': influencer_reach,
                'influencer_niche': influencer_niche,
                'influencer_platform': influencer_platform,
                'influencer_flagged': influencer_flagged
            }
            data.append(ad_request_info)

        return make_response(jsonify({"message": "Ad requests retrieved successfully", "data": data}), 200)


    @auth_required("token")
    @roles_accepted('sponsor')
    def put(self, adrequest_id):
        # Accept, reject, or mark as completed an ad request
        data = request.get_json()
        action = data.get('action')  # Expecting 'accept', 'reject', or 'markAsCompleted'
        sponsor_id = data.get('sponsor_id')  # The sponsor ID from the request body

        # Find the ad request by id
        ad_request = Adrequests.query.get(adrequest_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        # Find the campaign related to this ad request
        campaign = Campaigns.query.get(ad_request.campaign_id)
        if not campaign or int(campaign.sponsor_id) != int(sponsor_id):
            return make_response(jsonify({"message": "You are not authorized to modify this ad request"}), 403)

        # Check if the influencer or campaign is flagged
        influencer = Influencer.query.get(ad_request.influencer_id)

        # Validate actions based on flags
        if action == 'accept':
            if influencer.flagged or campaign.flagged:
                return make_response(jsonify({"message": "Cannot accept this request because it is flagged."}), 403)
            ad_request.status = 'accepted'
        
        elif action == 'reject':
            if influencer.flagged or campaign.flagged:
                return make_response(jsonify({"message": "Cannot reject this request because it is flagged."}), 403)
            ad_request.status = 'rejected'
        
        elif action == 'markAsCompleted':
            if ad_request.status != 'accepted':
                return make_response(jsonify({"message": "Request must be accepted before marking as completed."}), 400)
            ad_request.status = 'Completed'
        else:
            return make_response(jsonify({"message": "Invalid action"}), 400)

        try:
            db.session.commit()
            return make_response(jsonify({"message": f"Ad request {action}ed successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"Failed to {action} ad request: {str(e)}"}), 500)



class GetSponsorDetails(Resource):
    @auth_required("token")
    @roles_accepted('sponsor')
    def get(self, sponsor_id):
        try:
            # Find the sponsor
            sponsor = Sponsor.query.get(sponsor_id)
            if not sponsor:
                return make_response(jsonify({"message": "Sponsor not found"}), 404)

            # Return sponsor details
            return make_response(jsonify({
                "company_name": sponsor.company_name,
                "email": sponsor.email,
                "company_budget": sponsor.company_budget,
                "username": sponsor.username,
                "industry": sponsor.industry,
                "flagged": sponsor.flagged,
                "approved": sponsor.approved,
            }), 200)

        except Exception as e:
            return make_response(jsonify({"message": f"An error occurred: {str(e)}"}), 500)





class CampaignSearchResource(Resource):
    def get(self):
        query = request.args.get('query', '')
        cur_date = datetime.now()
        # Query campaigns based on name, description, goals, or niche and visibility
        campaigns = Campaigns.query.filter(
            (Campaigns.name.ilike(f'%{query}%') | 
             Campaigns.description.ilike(f'%{query}%') | 
             Campaigns.goals.ilike(f'%{query}%') | 
             Campaigns.niche.ilike(f'%{query}%')) &
            (Campaigns.visibility == 'public') &
            (Campaigns.end_date > cur_date) &
            (Campaigns.flagged != 1)
        ).all()

        if not campaigns:
            return {"data": [], "message": "No campaigns found"}, 404

        # Convert to serializable format
        campaign_data = [{
            'campaign_id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'niche': campaign.niche,
            'start_date': campaign.start_date.isoformat() if campaign.start_date else None,
            'end_date': campaign.end_date.isoformat() if campaign.end_date else None,
            'campaign_budget': campaign.campaign_budget,
            'visibility': campaign.visibility,
            'goals': campaign.goals
        } for campaign in campaigns]

        return {"data": campaign_data}, 200



class SponsorStatistics(Resource):
    @auth_required("token")
    @roles_accepted('sponsor')
    def get(self, sponsor_id):
        try:
            # Fetch all campaigns for the sponsor
            campaigns = Campaigns.query.filter_by(sponsor_id=sponsor_id).all()
            campaign_ids = [campaign.id for campaign in campaigns]

            total_adrequest_sent = Adrequests.query.filter(
                Adrequests.sent_by_sponsor == True,
                Adrequests.campaign_id.in_(campaign_ids)
            ).count()

            total_adrequest_received = Adrequests.query.filter(
                Adrequests.sent_by_sponsor == False,
                Adrequests.campaign_id.in_(campaign_ids)
            ).count()

            total_adrequest_accepted = Adrequests.query.filter(
                Adrequests.sent_by_sponsor == False,
                Adrequests.campaign_id.in_(campaign_ids),
                Adrequests.status.in_(['accepted', 'Completed'])
            ).count()

            total_adrequest_rejected = Adrequests.query.filter(
                Adrequests.sent_by_sponsor == False,
                Adrequests.campaign_id.in_(campaign_ids),
                Adrequests.status == 'rejected'
            ).count()

            total_completed_campaigns = Campaigns.query.filter_by(sponsor_id=sponsor_id, flagged=0).count()  # Assuming completed campaigns are flagged

            # Construct the response with the gathered statistics
            data = {
                'total_adrequest_sent': total_adrequest_sent,
                'total_adrequest_received': total_adrequest_received,
                'total_adrequest_accepted': total_adrequest_accepted,
                'total_adrequest_rejected': total_adrequest_rejected,
                'total_completed_campaigns': total_completed_campaigns
            }

            return make_response(jsonify({"message": "Sponsor statistics retrieved successfully", "data": data}), 200)

        except Exception as e:
            print(f"Error fetching sponsor statistics: {e}")
            return make_response(jsonify({"message": "An error occurred while fetching sponsor statistics"}), 500)


class Create_csv(Resource):
    def get(self):
        sponsor_id = request.args.get('sponsor_id')
        task = create_csv.delay(sponsor_id) 
        return {'task_id': task.id}, 200


class GetCSV(Resource):
    def get(self, id):
        result = AsyncResult(id)

        if result.ready():
            file_path = f'./instance/{result.result}'
            # Check if the file exists and is a file
            if os.path.exists(file_path) and os.path.isfile(file_path):
                try:
                    return send_file(file_path, as_attachment=True)
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            else:
                return jsonify({"error": "File not found"}), 404
        else:
            return jsonify({"message": "Task not ready"}), 202