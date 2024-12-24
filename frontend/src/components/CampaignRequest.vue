<template>
  <div>
    <h2>Campaign Requests</h2>

    <div class="campaign-container">
      <div v-for="campaign in campaigns" :key="campaign.campaign_id" class="campaign-card">
        <div class="campaign-header">
          <h3>{{ campaign.name }}</h3>
          <p class="niche">{{ campaign.niche }}</p>
        </div>
        <p><strong>Description:</strong> {{ campaign.description }}</p>
        <p><strong>Budget:</strong> {{ campaign.budget }}</p>
        <p><strong>Start Date:</strong> {{ campaign.start_date }}</p>
        <p><strong>End Date:</strong> {{ campaign.end_date }}</p>
        <p><strong>Visibility:</strong> {{ campaign.visibility }}</p>
        <p><strong>Goals:</strong> {{ campaign.goals }}</p>
        <p><strong>Status:</strong> {{ campaign.status }}</p>

        <div class="action-buttons">
          <button 
            v-if="campaign.flagged === 0" 
            @click="flagCampaign(campaign)" 
            class="btn flag-button">
            <i class="fa-solid fa-xmark"></i> Flag
          </button>
          <button 
            v-if="campaign.flagged === 1" 
            @click="unflagCampaign(campaign)" 
            class="btn unflag-button">
            <i class="fa-solid fa-flag"></i> Unflag
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CampaignRequest',
  data() {
    return {
      campaigns: []
    };
  },
  methods: {
    fetchCampaignRequests() {
      axios.get('http://127.0.0.1:5000/campaign_resources', {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken') 
        }
      })
      .then(response => {
        this.campaigns = response.data.data;
      })
      .catch(error => {
        console.error('Error fetching campaign requests:', error);
      });
    },

    flagCampaign(campaign) {
      axios.delete(`http://127.0.0.1:5000/admin/campaign/${campaign.campaign_id}/flagging`, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')  
        }
      })
      .then(() => {
        campaign.flagged = 1;
        this.fetchCampaignRequests();
        alert(`${campaign.name} flagged successfully!`);
      })
      .catch(error => {
        console.error('Error flagging campaign:', error);
        alert('Failed to flag the campaign.');
      });
    },

    unflagCampaign(campaign) {
      axios.delete(`http://127.0.0.1:5000/admin/campaign/${campaign.campaign_id}/unflagging`, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')  
        }
      })
      .then(() => {
        campaign.flagged = 0;
        this.fetchCampaignRequests();
        alert(`${campaign.name} unflagged successfully!`);
      })
      .catch(error => {
        console.error('Error unflagging campaign:', error);
        alert('Failed to unflag the campaign.');
      });
    }
  },

  created() {
    this.fetchCampaignRequests();
  }
};
</script>
<style scoped>
/* Campaign container to manage card layout */
.campaign-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  gap: 20px;
  margin-top: 20px;
}

/* Each campaign card */
.campaign-card {
  background-color: #009cd5;
  color: #fff;
  width: 300px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* .campaign-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
} */

/* Campaign header styling */
.campaign-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.niche {
  background-color: #000000;
  color: #adb5bd;
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 12px;
}

/* Action buttons */
.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

/* Button styles */
.btn {
  padding: 8px 12px;
  border-radius: 0px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s, transform 0.3s;
}

.flag-button {
  background-color: #dc3545; /* Red for flagging */
  color: white;
}

.flag-button:hover {
  background-color: #c82333;
  transform: scale(1.05);
}

.unflag-button {
  background-color: #ffc107; /* Yellow for unflagging */
  color: black;
}

.unflag-button:hover {
  background-color: #e0a800;
  transform: scale(1.05);
}
</style>

  