from flask_restful import Resource
from flask import jsonify, request, make_response
from datetime import datetime
from flask_security import roles_accepted, current_user
import sqlite3
from collections import defaultdict
from models import *

class SponsorApproval(Resource):
    def put(self, id):
        sponsor = Sponsor.query.get(id)
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)

        sponsor.approved = 1
        db.session.commit()
        return make_response(jsonify({"message": "Sponsor approved successfully"}), 200)

class SponsorResources(Resource):
    def get(self):
        try:
            sponsors = Sponsor.query.all()
            sponsor_list = []
            for sponsor in sponsors:
                sponsor_list.append({
                    'sponsor_id': sponsor.id,
                    'sponsor_name': sponsor.username,
                    'email': sponsor.email,
                    'company_name': sponsor.company_name,
                    'industry': sponsor.industry,
                    'budget': sponsor.company_budget,
                    'status': 'pending' if not sponsor.approved else 'approved',
                    'flagged': sponsor.flagged
                })
            return make_response(jsonify({'data': sponsor_list}), 200)
        except Exception as e:
            print(f"Error fetching sponsors: {e}")  # Log the error
            return make_response(jsonify({'message': 'Error fetching sponsor requests'}), 500)

class SponsorFlagging(Resource):
    def delete(self, id):
        sponsor = Sponsor.query.get(id)
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        sponsor.flagged = 1
        campaigns = Campaigns.query.filter_by(sponsor_id=id).all()
        if campaigns:
            for campaign in campaigns:
                campaign.flagged = 1 
        db.session.commit()
        return make_response(jsonify({"message": "Sponsor and associated campaigns flagged successfully"}), 200)

class SponsorUnFlagging(Resource):
    def delete(self, id):
        sponsor = Sponsor.query.get(id)
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        
        sponsor.flagged = 0
        campaigns = Campaigns.query.filter_by(sponsor_id=id).all()
        if campaigns:
            for campaign in campaigns:
                campaign.flagged = 0 
        db.session.commit()

        return make_response(jsonify({"message": "Sponsor and associated Unflagged successfully"}), 200)



class InfluencerResources(Resource):
    def get(self):
        try:
            influencers = Influencer.query.all()
            influencer_list = []
            for influencer in influencers:
                influencer_list.append({
                    'influencer_id': influencer.id,
                    'name': influencer.name,
                    'email': influencer.email,
                    'category': influencer.category,
                    'reach': influencer.reach,
                    'niche': influencer.niche,
                    'platform': influencer.platform,
                    'flagged': influencer.flagged,
                    'status': 'flagged' if influencer.flagged else 'active'
                })
            return make_response(jsonify({'data': influencer_list}), 200)
        except Exception as e:
            print(f"Error fetching influencers: {e}")  # Log the error
            return make_response(jsonify({'message': 'Error fetching influencer requests'}), 500)




class InfluencerFlagging(Resource):
    def delete(self, id):
        influencer = Influencer.query.get(id)
        if not influencer:
            return make_response(jsonify({"message": "Influencer not found"}), 404)
        
        influencer.flagged = 1
        db.session.commit()
        
        return make_response(jsonify({"message": "Influencer flagged successfully"}), 200)
    

class InfluencerUnFlagging(Resource):
    def delete(self, id):
        influencer = Influencer.query.get(id)
        if not influencer:
            return make_response(jsonify({"message": "Influencer not found"}), 404)
        
        influencer.flagged = 0
        db.session.commit()
        
        return make_response(jsonify({"message": "Influencer Unflagged successfully"}), 200)
    


class CampaignResources(Resource):
    def get(self):
        try:
            campaigns = Campaigns.query.all()
            campaign_list = []

            for campaign in campaigns:
                campaign_list.append({
                    'campaign_id': campaign.id,
                    'name': campaign.name,
                    'niche': campaign.niche,
                    'description': campaign.description,
                    'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                    'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                    'budget': campaign.campaign_budget,
                    'visibility': campaign.visibility,
                    'goals': campaign.goals,
                    'flagged': campaign.flagged,
                    'status': 'flagged' if campaign.flagged else 'not flagged'
                })

            return make_response(jsonify({'data': campaign_list}), 200)
        
        except Exception as e:
            print(f"Error fetching campaigns: {e}")
            return make_response(jsonify({'message': 'Error fetching campaign data'}), 500)
        
class CampaignFlagging(Resource):
    def delete(self, id):
        campaign = Campaigns.query.get(id)
        if not campaign:
            return make_response(jsonify({"message": "Campaign not found"}), 404)
        campaign.flagged = 1
        db.session.commit()
        return make_response(jsonify({"message": "Campaign flagged successfully"}), 200)


class CampaignUnFlagging(Resource):
    def delete(self, id):
        
        campaign = Campaigns.query.get(id)
        
        if not campaign:
            return make_response(jsonify({"message": "Campaign not found"}), 404)
        campaign.flagged = 0
        db.session.commit()
        return make_response(jsonify({"message": "Campaign unflagged successfully"}), 200)


# admin stats

class AdminOverallStatistics(Resource):
    def get(self):
        try:
            # Total counts
            total_sponsors = Sponsor.query.count()
            total_influencers = Influencer.query.count()
            total_campaigns = Campaigns.query.count()
            total_ads = Adrequests.query.count()

            # Flagged vs Non-Flagged Influencers
            flagged_influencers = Influencer.query.filter_by(flagged=True).count()
            non_flagged_influencers = total_influencers - flagged_influencers

            # Flagged vs Non-Flagged Sponsors
            flagged_sponsors = Sponsor.query.filter_by(flagged=True).count()
            non_flagged_sponsors = total_sponsors - flagged_sponsors

            # Flagged vs Non-Flagged Campaigns
            flagged_campaigns = Campaigns.query.filter_by(flagged=True).count()
            non_flagged_campaigns = total_campaigns - flagged_campaigns

            # Public vs Private Campaigns
            public_campaigns = Campaigns.query.filter_by(visibility='public').count()
            private_campaigns = total_campaigns - public_campaigns

            # Influencer counts by niche
            niche_counts = (
                db.session.query(Influencer.niche, db.func.count(Influencer.id))
                .group_by(Influencer.niche)
                .all()
            )
            niche_distribution = defaultdict(int)
            for niche, count in niche_counts:
                niche_distribution[niche] = count

            # Distribution of campaigns by budget
            budget_distribution = (
                db.session.query(Campaigns.campaign_budget, db.func.count(Campaigns.id))
                .group_by(Campaigns.campaign_budget)
                .all()
            )
            budget_counts = defaultdict(int)
            for budget, count in budget_distribution:
                budget_counts[budget] = count

            # Distribution of influencers by reach
            reach_distribution = (
                db.session.query(Influencer.reach, db.func.count(Influencer.id))
                .group_by(Influencer.reach)
                .all()
            )
            reach_counts = defaultdict(int)
            for reach, count in reach_distribution:
                reach_counts[reach] = count

            # Response data
            data = {
                'total_sponsors': total_sponsors,
                'total_influencers': total_influencers,
                'total_campaigns': total_campaigns,
                'total_ads': total_ads,
                'flagged_influencers': flagged_influencers,
                'non_flagged_influencers': non_flagged_influencers,
                'flagged_sponsors': flagged_sponsors,
                'non_flagged_sponsors': non_flagged_sponsors,
                'flagged_campaigns': flagged_campaigns,
                'non_flagged_campaigns': non_flagged_campaigns,
                'public_campaigns': public_campaigns,
                'private_campaigns': private_campaigns,
                'niche_distribution': dict(niche_distribution),  # Niche distribution
                'budget_distribution': dict(budget_counts),      # New budget distribution
                'reach_distribution': dict(reach_counts),        # New reach distribution
            }

            return make_response(jsonify({"message": "Statistics retrieved successfully", "data": data}), 200)

        except Exception as e:
            print(f"Error fetching admin statistics: {e}")  # Log the error
            return make_response(jsonify({'message': 'Error fetching statistics'}), 500)
