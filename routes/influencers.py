from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_required, roles_accepted, current_user
from datetime import datetime, date
from models import *
from caching import cache


class ActiveInfluencers(Resource):
    def get(self):
        try:
            influencers = Influencer.query.filter(Influencer.flagged != 1).all()
            influencer_list = []
            for influencer in influencers:
                influencer_list.append({
                    'influencer_id': influencer.id,
                    'name': influencer.name,
                    'category': influencer.category,
                    'reach': influencer.reach,
                    'niche': influencer.niche,
                    'platform': influencer.platform,
                    'flagged': influencer.flagged,
                    'status': 'active'
                })
            return make_response(jsonify({'data': influencer_list}), 200)
        except Exception as e:
            print(f"Error fetching active influencers: {e}")
            return make_response(jsonify({'message': 'Error fetching active influencers'}), 500)




class PublicCampaigns(Resource):
    def get(self):
        try:
            # Get the current date
            today = datetime.today().date()

            # Query to get campaigns that are not flagged, have public visibility, and end date is in the future
            campaigns = Campaigns.query.filter(
                Campaigns.flagged != 1,
                Campaigns.visibility == 'public',
                Campaigns.end_date >= today  # Only campaigns with end_date in the future
            ).all()

            campaign_list = []
            for campaign in campaigns:
                sponsor = campaign.sponsor  # Access the sponsor relationship
                campaign_list.append({
                    'campaign_id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'campaign_budget': campaign.campaign_budget,
                    'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                    'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                    'visibility': campaign.visibility,
                    'goals': campaign.goals,
                    'niche': campaign.niche,
                    'status': 'public',
                    'sponsor_name': sponsor.username if sponsor else 'Unknown'  # Get sponsor's username
                })
                
            return make_response(jsonify({'data': campaign_list}), 200)
        except Exception as e:
            print(f"Error fetching public campaigns: {e}")
            return make_response(jsonify({'message': 'Error fetching public campaigns'}), 500)





class SubmitInfluencerAdRequest(Resource):
    def post(self):
        try:
            # Get the data from the POST request
            data = request.get_json()
            influencer_id = data.get('influencer_id')
            campaign_id = data.get('campaign_id')
            message = data.get('message')
            requirements = data.get('requirements')
            payment = data.get('payment')

            # Validate input
            if not influencer_id or not campaign_id or not message or payment <= 0:
                return make_response(jsonify({'message': 'Invalid input'}), 400)

            # Check if campaign exists
            campaign = Campaigns.query.get(campaign_id)
            if not campaign:
                return make_response(jsonify({'message': 'Campaign not found'}), 404)

            # Check if the influencer is active and exists
            influencer = Influencer.query.get(influencer_id)
            if not influencer or influencer.flagged == 1:
                return make_response(jsonify({'message': 'Influencer not found or inactive'}), 404)

            # Create the Ad Request
            ad_request = Adrequests(
                influencer_id=influencer_id,
                # sponsor_id=campaign.sponsor_id,  # Assuming the sponsor created the campaign
                campaign_id=campaign_id,
                messages=message,
                requirements=requirements,
                payment_amt=payment,
                status='Pending',
                sent_by_sponsor=False,
            )

            # Add the ad request to the database
            db.session.add(ad_request)
            db.session.commit()

            return make_response(jsonify({'message': 'Ad request submitted successfully!'}), 201)

        except Exception as e:
            print(f"Error in SubmitInfluencerAdRequest: {e}")
            return make_response(jsonify({'message': 'An error occurred. Please try again.'}), 500)
        

class InfluencerAdRequestResource(Resource):
    @auth_required("token")
    @cache.cached(timeout = 2)
    @roles_accepted('influencer')
    def get(self, influencer_id): 
        # Fetch ad requests with additional details (campaign name, sponsor name, and flagged status)
        ad_requests = (
            db.session.query(
                Adrequests,
                Campaigns.name.label('campaign_name'),
                Campaigns.flagged.label('campaign_flagged'),  # Fetch campaign flagged status
                Sponsor.username.label('sponsor_name'),
                Sponsor.flagged.label('sponsor_flagged')  # Fetch sponsor flagged status
            )
            .join(Campaigns, Adrequests.campaign_id == Campaigns.id)
            .join(Sponsor, Campaigns.sponsor_id == Sponsor.id)
            .filter(Adrequests.influencer_id == influencer_id, Adrequests.sent_by_sponsor.is_(False))
            .all()
        )

        if not ad_requests:
            return make_response(jsonify({"message": "No ad requests found for this influencer."}), 404)

        data = []
        for ad_request, campaign_name, campaign_flagged, sponsor_name, sponsor_flagged in ad_requests:
            ad_request_info = {
                'id': ad_request.id,
                'messages': ad_request.messages,
                'requirements': ad_request.requirements,
                'status': ad_request.status,
                'payment_amt': ad_request.payment_amt,
                'campaign_id': ad_request.campaign_id,
                'campaign_name': campaign_name,
                'campaign_flagged': campaign_flagged,  # Include campaign flagged status
                'sponsor_flagged': sponsor_flagged,    # Include sponsor flagged status
                'influencer_id': ad_request.influencer_id,
                'sponsor_name': sponsor_name if sponsor_name else "N/A",
            }
            data.append(ad_request_info)

        return make_response(jsonify({"message": "Ad requests retrieved successfully", "data": data}), 200)


class InfluencerAdRequestSpecificResource(Resource):
    @auth_required("token")
    @cache.cached(timeout = 2)
    @roles_accepted('influencer')
    def get(self, adrequest_id):
        # Retrieve an ad request by ID
        ad_request = Adrequests.query.get(adrequest_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        # Ensure the ad request belongs to the influencer making the request
        if ad_request.influencer_id != ad_request.influencer_id:  # This check might be unnecessary, see below
            return make_response(jsonify({"message": "You are not authorized to access this ad request"}), 403)

        # Convert ad_request to a dictionary and return it
        return make_response(jsonify({
            "data": {
                "messages": ad_request.messages,
                "requirements": ad_request.requirements,
                "status": ad_request.status,
                "payment_amt": ad_request.payment_amt,
                "campaign_id": ad_request.campaign_id,
                "influencer_id": ad_request.influencer_id,
                "sent_by_sponsor": ad_request.sent_by_sponsor
            }
        }), 200)

    @auth_required("token")
    @roles_accepted('influencer')
    def put(self, adrequest_id):
        # Update an ad request
        data = request.get_json()

        # Find the ad request by id
        ad_request = Adrequests.query.get(adrequest_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        # Ensure the ad request belongs to the influencer making the request
        if ad_request.influencer_id != ad_request.influencer_id:  # This check might be unnecessary, see below
            return make_response(jsonify({"message": "You are not authorized to update this ad request"}), 403)

        # Update the fields of the ad request
        ad_request.messages = data.get('messages', ad_request.messages)
        ad_request.requirements = data.get('requirements', ad_request.requirements)
        ad_request.status = data.get('status', ad_request.status)
        ad_request.payment_amt = data.get('payment_amt', ad_request.payment_amt)

        try:
            db.session.commit()
            return make_response(jsonify({"message": "Ad request updated successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"Failed to update ad request: {str(e)}"}), 500)

    @auth_required("token")
    @roles_accepted('influencer')
    def delete(self, adrequest_id):
        # Delete an ad request by id
        ad_request = Adrequests.query.get(adrequest_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        # Ensure the ad request belongs to the influencer making the request
        if ad_request.influencer_id != ad_request.influencer_id:  # This check might be unnecessary, see below
            return make_response(jsonify({"message": "You are not authorized to delete this ad request"}), 403)

        try:
            db.session.delete(ad_request)
            db.session.commit()
            return make_response(jsonify({"message": "Ad request deleted successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"Failed to delete ad request: {str(e)}"}), 500)



class InfluencerReceivedAdRequestResource(Resource):
    @auth_required("token")
    @cache.cached(timeout=2)
    @roles_accepted('influencer')
    def get(self, influencer_id): 
        # Fetch ad requests for this influencer with campaign and sponsor flagged status
        ad_requests = (
            db.session.query(
                Adrequests,
                Campaigns.name.label('campaign_name'),
                Campaigns.start_date.label('start_date'),
                Campaigns.end_date.label('end_date'),
                Campaigns.flagged.label('campaign_flagged'),  # Include flagged status
                Sponsor.username.label('sponsor_name'),
                Sponsor.flagged.label('sponsor_flagged')  # Include sponsor flagged status
            )
            .join(Campaigns, Adrequests.campaign_id == Campaigns.id)
            .join(Sponsor, Campaigns.sponsor_id == Sponsor.id)
            .filter(Adrequests.influencer_id == influencer_id, Adrequests.sent_by_sponsor.is_(True))
            .all()
        )

        if not ad_requests:
            return make_response(jsonify({"message": "No ad requests found for this influencer."}), 404)

        data = []
        current_date = date.today()
        for ad_request, campaign_name, start_date, end_date, campaign_flagged, sponsor_name, sponsor_flagged in ad_requests:
            ad_request_info = {
                'id': ad_request.id,
                'messages': ad_request.messages,
                'requirements': ad_request.requirements,
                'status': ad_request.status,
                'payment_amt': ad_request.payment_amt,
                'campaign_name': campaign_name,
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None,
                'is_expired': end_date < current_date if end_date else False,  # Check if end_date is in the past
                'campaign_flagged': campaign_flagged,  # Include flagged status in response
                'sponsor_name': sponsor_name if sponsor_name else "N/A",
                'sponsor_flagged': sponsor_flagged  # Include sponsor flagged status
            }
            data.append(ad_request_info)

        return make_response(jsonify({"message": "Ad requests retrieved successfully", "data": data}), 200)


    @auth_required("token")
    @roles_accepted('influencer')
    def put(self, adrequest_id):
        # Accept or reject an ad request
        data = request.get_json()
        action = data.get('action')  # Expecting 'accept' or 'reject'
        influencer_id = data.get('influencer_id')  # The influencer ID from the request body

        # Find the ad request by id
        ad_request = Adrequests.query.get(adrequest_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        # Ensure the ad request belongs to the influencer making the request
        if str(ad_request.influencer_id) != str(influencer_id):
            return make_response(jsonify({"message": "You are not authorized to modify this ad request"}), 403)

        # Perform the requested action
        if action == 'accept':
            ad_request.status = 'accepted'
        elif action == 'reject':
            ad_request.status = 'rejected'
        else:
            return make_response(jsonify({"message": "Invalid action"}), 400)

        try:
            db.session.commit()
            return make_response(jsonify({"message": f"Ad request {action}ed successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"Failed to {action} ad request: {str(e)}"}), 500)




class UpdateInfluencerDetails(Resource):
    @auth_required("token")
    @roles_accepted('influencer')
    def put(self, influencer_id):
        try:
            # Get the new data from the request body
            data = request.get_json()
            new_category = data.get('category')
            new_niche = data.get('niche')
            new_reach = data.get('reach')
            new_platform = data.get('platform')  # Get platform from request body

            # Validate the new data
            if not new_category or not new_niche or not isinstance(new_reach, int) or not new_platform:
                return make_response(jsonify({"message": "Invalid input"}), 400)

            # Find the influencer and update details
            influencer = Influencer.query.get(influencer_id)
            if not influencer:
                return make_response(jsonify({"message": "Influencer not found"}), 404)

            influencer.category = new_category
            influencer.niche = new_niche
            influencer.reach = new_reach
            influencer.platform = new_platform  # Update platform

            # Commit changes
            db.session.commit()

            return make_response(jsonify({"message": "Influencer details updated successfully"}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"An error occurred: {str(e)}"}), 500)

        

class GetInfluencerDetails(Resource):
    @auth_required("token")
    @cache.cached(timeout = 2)
    @roles_accepted('influencer')
    def get(self, influencer_id):
        try:
            # Find the influencer
            influencer = Influencer.query.get(influencer_id)
            if not influencer:
                return make_response(jsonify({"message": "Influencer not found"}), 404)

            # Return influencer details
            return make_response(jsonify({
                "username": influencer.username,
                "category": influencer.category,
                "email": influencer.email,
                "niche": influencer.niche,
                "reach": influencer.reach,
                "platform": influencer.platform,
            }), 200)

        except Exception as e:
            return make_response(jsonify({"message": f"An error occurred: {str(e)}"}), 500)


class InfluencerResource(Resource):
    def get(self):
        query = request.args.get('query', '')

        # Query influencers based on name, niche, industry, or platform
        influencers = Influencer.query.filter(
            (Influencer.name.ilike(f'%{query}%') | 
            Influencer.niche.ilike(f'%{query}%') | 
            Influencer.category.ilike(f'%{query}%') | 
            Influencer.platform.ilike(f'%{query}%')) &
            (Influencer.flagged != 1)
        ).all()

        if not influencers:
            return {"data": [], "message": "No influencers found"}, 404

        # Convert to serializable format
        influencer_data = [{
            'influencer_id': inf.id,
            'name': inf.name,
            'category': inf.category,
            'reach': inf.reach,
            'niche': inf.niche,
            'platform': inf.platform
        } for inf in influencers]

        return {"data": influencer_data}, 200



class InfluencerStatistics(Resource):
    @auth_required("token")
    @cache.cached(timeout = 2)
    @roles_accepted('influencer')
    def get(self, influencer_id):
        try:
            # Fetch the total number of ad requests sent by the influencer
            total_adrequest_sent = Adrequests.query.filter_by(influencer_id=influencer_id, sent_by_sponsor=False).count()

            # Fetch the total number of ad requests received by the influencer
            total_adrequest_received = Adrequests.query.filter_by(influencer_id=influencer_id, sent_by_sponsor=True).count()

            # Fetch the total number of ad requests accepted by the influencer
            total_adrequest_accepted = Adrequests.query.filter(
                Adrequests.influencer_id == influencer_id,
                Adrequests.status.in_(['accepted', 'Completed']),
                Adrequests.sent_by_sponsor == True
            ).count()

            total_adrequest_rejected = Adrequests.query.filter_by(influencer_id=influencer_id, status='rejected',  sent_by_sponsor=True).count()
            # Fetch total completed campaigns where the influencer participated
            total_completed_campaigns = (
                Campaigns.query
                .join(Adrequests, Campaigns.id == Adrequests.campaign_id)
                .filter(Adrequests.influencer_id == influencer_id, Campaigns.end_date <= datetime.today(), Adrequests.status == "Completed")
                .count()
            )

            # Construct the response with the gathered statistics
            data = {
                'total_adrequest_sent': total_adrequest_sent,
                'total_adrequest_received': total_adrequest_received,
                'total_adrequest_accepted': total_adrequest_accepted,
                'total_adrequest_rejected': total_adrequest_rejected,
                'total_completed_campaigns': total_completed_campaigns
            }

            return make_response(jsonify({"message": "Influencer statistics retrieved successfully", "data": data}), 200)

        except Exception as e:
            print(f"Error fetching influencer statistics: {e}")
            return make_response(jsonify({"message": "An error occurred while fetching statistics"}), 500)
