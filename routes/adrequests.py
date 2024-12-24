from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_required, roles_accepted
from datetime import datetime
from models import Adrequests, db, Influencer, Campaigns
from caching import cache

class AdRequestResource(Resource):

    @auth_required("token")
    @roles_accepted('admin', 'sponsor', 'influencer')
    def post(self):
        data = request.get_json()

        # Extracting required fields from the request data
        messages = data.get('message')
        requirements = data.get('requirements')
        payment_amt = data.get('payment')
        campaign_id = data.get('campaign_id')
        influencer_id = data.get('influencer_id')

        # Error handling for mandatory fields
        if not messages or not requirements:
            return make_response(jsonify({"message": "Message and requirements are required."}), 400)
        if payment_amt is None:
            return make_response(jsonify({"message": "Payment amount is required."}), 400)
        if not campaign_id or not influencer_id:
            return make_response(jsonify({"message": "Campaign ID and Influencer ID are required."}), 400)

        # Fetch the campaign's budget from the database
        campaign = Campaigns.query.get(campaign_id)
        if not campaign:
            return make_response(jsonify({"message": "Campaign not found."}), 404)

        if payment_amt > campaign.campaign_budget:  # Assuming 'budget' is a field in your Campaign model
            return make_response(jsonify({"message": "Payment amount exceeds the campaign budget."}), 400)

        # Create a new Adrequest object
        ad_request = Adrequests(
            messages=messages,
            requirements=requirements,
            status='Pending',  # Default status
            payment_amt=payment_amt,
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            sent_by_sponsor=True,
        )

        # Add and commit to the database
        db.session.add(ad_request)
        db.session.commit()

        return make_response(jsonify({"message": "Ad request created successfully", "ad_request_id": ad_request.id}), 201)


    @auth_required("token")
    @cache.cached(timeout = 2)
    @roles_accepted('admin', 'sponsor', 'influencer')
    def get(self):
        # Optional filtering based on campaign ID and influencer ID
        campaign_id = request.args.get('campaign_id')
        influencer_id = request.args.get('influencer_id')

        # Query ad requests based on the provided filters
        query = Adrequests.query

        if campaign_id:
            query = query.filter_by(campaign_id=campaign_id)
        if influencer_id:
            query = query.filter_by(influencer_id=influencer_id)

        ad_requests = query.all()

        # Check if any ad requests were found
        if not ad_requests:
            return make_response(jsonify({"message": "No ad requests found."}), 404)

        # Prepare response data
        data = []
        for ad_request in ad_requests:
            ad_request_info = {
                'id': ad_request.id,
                'messages': ad_request.messages,
                'requirements': ad_request.requirements,
                'status': ad_request.status,
                'payment_amt': ad_request.payment_amt,
                'campaign_id': ad_request.campaign_id,
                'influencer_id': ad_request.influencer_id,
            }
            data.append(ad_request_info)

        return make_response(jsonify({"message": "Ad requests retrieved successfully", "data": data}), 200)


class SponsorAdRequestResource(Resource):
    @auth_required("token")
    @cache.cached(timeout=2)
    @roles_accepted('sponsor')
    def get(self, sponsor_id):
        # Fetch ad requests with additional details (influencer name, campaign name, flagged status for both influencer and campaign)
        ad_requests = (
            db.session.query(
                Adrequests,
                Campaigns.name.label('campaign_name'),
                Campaigns.flagged.label('campaign_flagged'),  # Add campaign flagged status
                Campaigns.end_date.label('end_date'),  # Add campaign end date
                Influencer.name.label('influencer_name'),
                Influencer.flagged.label('influencer_flagged')
            )
            .join(Campaigns, Adrequests.campaign_id == Campaigns.id)
            .outerjoin(Influencer, Adrequests.influencer_id == Influencer.id)
            .filter(Campaigns.sponsor_id == sponsor_id, Adrequests.sent_by_sponsor.is_(True))  # Filter for sponsor-sent requests
            .all()
        )

        if not ad_requests:
            return make_response(jsonify({"message": "No ad requests found for this sponsor."}), 404)

        current_date = datetime.now().date()  # Get the current date
        data = []
        for ad_request, campaign_name, campaign_flagged, end_date, influencer_name, influencer_flagged in ad_requests:
            ad_request_info = {
                'id': ad_request.id,
                'messages': ad_request.messages,
                'requirements': ad_request.requirements,
                'status': ad_request.status,
                'payment_amt': ad_request.payment_amt,
                'campaign_id': ad_request.campaign_id,
                'campaign_name': campaign_name,
                'campaign_flagged': campaign_flagged,  # Add campaign flagged status
                'influencer_id': ad_request.influencer_id,
                'influencer_name': influencer_name if influencer_name else "N/A",
                'influencer_flagged': influencer_flagged,  # Include influencer flagged status
                'end_date': end_date.isoformat() if end_date else None,  # Include campaign end date
                'is_expired': end_date < current_date if end_date else False  # Compute expired status
            }
            data.append(ad_request_info)

        return make_response(jsonify({"message": "Ad requests retrieved successfully", "data": data}), 200)





class AdrequestSpecificResource(Resource):
    @auth_required("token")
    @cache.cached(timeout = 2)
    @roles_accepted('sponsor')
    def get(self, adrequest_id):
        # Retrieve an ad request by ID
        ad_request = Adrequests.query.get(adrequest_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        # Convert ad_request to a dictionary and return it
        return make_response(jsonify({
            "data": {
                "messages": ad_request.messages,
                "requirements": ad_request.requirements,
                "status": ad_request.status,
                "payment_amt": ad_request.payment_amt
            }
        }), 200)
    @auth_required("token")
    @roles_accepted('sponsor')
    def put(self, adrequest_id):
        # Update an ad request
        data = request.get_json()

        # Find the ad request by id
        ad_request = Adrequests.query.get(adrequest_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        # Assuming you have a Campaign model to get the budget
        campaign = Campaigns.query.get(ad_request.campaign_id)  # Adjust this line as necessary
        if not campaign:
            return make_response(jsonify({"message": "Campaign not found"}), 404)

        payment_amt = data.get('payment_amt', ad_request.payment_amt)
        if payment_amt > campaign.campaign_budget:
            return make_response(jsonify({"message": "Payment amount exceeds campaign budget."}), 400)

        # Update the fields of the ad request
        ad_request.messages = data.get('messages', ad_request.messages)
        ad_request.requirements = data.get('requirements', ad_request.requirements)
        ad_request.status = data.get('status', ad_request.status)
        ad_request.payment_amt = payment_amt  # Update to the new payment amount

        try:
            db.session.commit()
            return make_response(jsonify({"message": "Ad request updated successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"Failed to update ad request: {str(e)}"}), 500)


    @auth_required("token")
    @roles_accepted('sponsor')
    def delete(self, adrequest_id):
        # Delete an ad request by id
        ad_request = Adrequests.query.get(adrequest_id)
        if not ad_request:
            return make_response(jsonify({"message": "Ad request not found"}), 404)

        try:
            db.session.delete(ad_request)
            db.session.commit()
            return make_response(jsonify({"message": "Ad request deleted successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": f"Failed to delete ad request: {str(e)}"}), 500)







