<template>
  <div>
    <h2>All Campaigns</h2>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    <div v-else>
      <div v-for="campaign in campaigns" :key="campaign.id" class="campaign-card">
        <h3>{{ campaign.name }}</h3>
        <p><strong>Description:</strong> {{ campaign.description }}</p>
        <p><strong>Niche:</strong> {{ campaign.niche }}</p>
        <p><strong>Start Date:</strong> {{ campaign.start_date }}</p>
        <p><strong>End Date:</strong> {{ campaign.end_date }}</p>
        <p><strong>Budget:</strong> {{ campaign.budget }}</p>
        <p><strong>Visibility:</strong> {{ campaign.visibility }}</p>
        <p><strong>Goals:</strong> {{ campaign.goals }}</p>

        <!-- Conditional rendering for flagged campaigns -->
        <p v-if="campaign.flagged === 1" class="warning"><strong>Message:</strong> This campaign is flagged!</p>

        <!-- Render buttons, but disable them if the campaign is flagged or has ended -->
        <div class="button-group">
          <button 
            @click="editCampaign(campaign.id)" 
            :disabled="campaign.flagged === 1 || !isCampaignActive(campaign.end_date)"
            :class="{ 'disabled-button': campaign.flagged === 1 || !isCampaignActive(campaign.end_date) }"
          >
            Edit
          </button>
          <button 
            @click="deleteCampaign(campaign.id)" 
            :disabled="campaign.flagged === 1 || !isCampaignActive(campaign.end_date)"
            :class="{ 'disabled-button': campaign.flagged === 1 || !isCampaignActive(campaign.end_date) }"
          >
            Delete
          </button>
          <button 
            @click="sendAdRequest(campaign)" 
            class="ad-request-button"
            :disabled="campaign.flagged === 1 || !isCampaignActive(campaign.end_date)"
            :class="{ 'disabled-button': campaign.flagged === 1 || !isCampaignActive(campaign.end_date) }"
          >
            Send Ad Request
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      campaigns: [],
      errorMessage: '',
    };
  },
  mounted() {
    this.fetchCampaigns();
  },
  methods: {
    async fetchCampaigns() {
      const token = localStorage.getItem('authToken');
      const sponsorId = localStorage.getItem('sponsor_id'); // Assuming sponsor ID is stored here
      if (!token) {
        this.errorMessage = 'No authentication token found.';
        return;
      }

      if (!sponsorId) {
        this.errorMessage = 'No sponsor ID found.';
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/sponsor/campaign', {
          method: 'GET',
          headers: {
            'Authentication-Token': token,
            'Sponsor-ID': sponsorId,
          },
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Failed to fetch campaigns');
        }

        this.campaigns = data.data;
      } catch (error) {
        this.errorMessage = error.message; 
      }
    },

    // Method to delete a campaign
    async deleteCampaign(id) {
      const token = localStorage.getItem('authToken');
      try {
        const response = await fetch(`http://127.0.0.1:5000/sponsor/campaign/${id}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': token,
          },
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to delete campaign');
        }

        // Remove the deleted campaign from the list
        this.campaigns = this.campaigns.filter(campaign => campaign.id !== id);
      } catch (error) {
        this.errorMessage = error.message;
      }
    },

    // Navigate to edit campaign page
    editCampaign(id) {
      this.$router.push(`/edit-campaign/${id}`);
    },

    // Navigate to the available influencers page
    sendAdRequest(campaign) { // Accept the whole campaign object
      this.$router.push({
        name: 'AvailableInfluencers',
        params: {
          campaignId: campaign.id,
          campaignName: campaign.name // Pass the campaign name
        }
      });
    },

    // Helper method to check if the campaign is still active
    isCampaignActive(endDate) {
      const today = new Date();
      const campaignEndDate = new Date(endDate);
      return campaignEndDate >= today; // Check if the campaign end date is in the future or today
    },
  },
};
</script>

<style scoped>
/* Same styles as before */

.campaign-card {
  background-color: #f4f4f4;
  padding: 20px;
  margin: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.error {
  color: red;
  font-weight: bold;
}

.warning {
  color: orange;
  font-weight: bold;
}

.button-group {
  margin-top: 15px;
}

button {
  margin-right: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

button:nth-of-type(2) {
  background-color: red;
}

button:nth-of-type(2):hover {
  background-color: darkred;
}

.ad-request-button {
  background-color: #28a745; /* Green color for the Ad Request button */
}

.ad-request-button:hover {
  background-color: #218838; /* Darker green on hover */
}

/* Disabled button styling */
button.disabled-button {
  background-color: rgb(114, 114, 114);
  cursor: not-allowed;
}

button.disabled-button:hover {
  background-color: grey; /* Prevent color change on hover */
}
</style>
