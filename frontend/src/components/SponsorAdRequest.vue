<template>
  <div class="sponsor-adrequests">
    <h2>Sent Ad Requests</h2>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="!adRequests.length && !errorMessage" class="no-requests-message">No ad requests found.</div>
    <ul>
      <li v-for="adRequest in adRequests" :key="adRequest.id" class="adrequest-item">
        <p><strong>Campaign Name:</strong> {{ adRequest.campaign_name }}</p>
        <p><strong>Influencer Name:</strong> {{ adRequest.influencer_name }}</p>
        <p><strong>Message:</strong> {{ adRequest.messages }}</p>
        <p><strong>Requirements:</strong> {{ adRequest.requirements }}</p>
        <p><strong>Acceptance Status:</strong> {{ adRequest.status }}</p>
        <p><strong>Payment Amount:</strong> {{ adRequest.payment_amt }}</p>

        <!-- Flagged message if either the influencer or the campaign is flagged, but only if not completed -->
        <p v-if="adRequest.campaign_flagged === 1 && adRequest.status !== 'Completed'" class="flagged-message">
          This campaign is flagged and cannot proceed further.
        </p>
        <p v-if="adRequest.influencer_flagged === 1 && adRequest.status !== 'Completed'" class="flagged-message">
          This influencer is flagged and cannot proceed further.
        </p>

        <!-- Completion status -->
        <p v-if="adRequest.status === 'Completed'" class="completed-message">
          This request has been successfully completed.
        </p>
        <p v-else-if="adRequest.status === 'accepted'" class="completion-status">
          <strong>Completion Status:</strong> Not completed
        </p>
        
        <p v-if="adRequest.is_expired" class="expired-message">
            This campaign has expired and no further action can be taken.
        </p>

        <div class="button-group">
          <!-- Show Edit button only if the status is 'Pending', campaign is not flagged, and influencer is not flagged -->
          <button v-if="adRequest.status === 'Pending' && adRequest.campaign_flagged === 0 && adRequest.influencer_flagged === 0 && !adRequest.is_expired" 
                  @click="editAdRequest(adRequest.id)" 
                  class="edit-button">Edit</button>
          
          <!-- Show Delete button if status is neither 'Accepted' nor 'Completed' -->
          <button v-if="adRequest.status !== 'accepted' && adRequest.status !== 'Completed'" 
                  @click="deleteAdRequest(adRequest.id)" 
                  :disabled="adRequest.campaign_flagged === 1 || adRequest.influencer_flagged === 1"
                  :class="{ 'disabled-button': adRequest.campaign_flagged === 1 || adRequest.influencer_flagged === 1 }"
                  class="delete-button">Delete</button>

          <!-- Show Mark as Completed if the status is 'Accepted', but disable if flagged -->
          <button v-if="adRequest.status === 'accepted'" 
                  @click="markAsCompleted(adRequest.id)" 
                  :disabled="adRequest.campaign_flagged === 1 || adRequest.influencer_flagged === 1"
                  :class="{ 'disabled-button': adRequest.campaign_flagged === 1 || adRequest.influencer_flagged === 1 }"
                  class="complete-button">Mark as Completed</button>
        </div>
      </li>
    </ul>
  </div>
</template>


<script>
export default {
  data() {
    return {
      adRequests: [],
      errorMessage: '',
    };
  },
  mounted() {
    this.fetchAdRequests();
  },
  methods: {
    async fetchAdRequests() {
      const token = localStorage.getItem('authToken');
      const sponsorId = localStorage.getItem('sponsor_id');

      if (!sponsorId) {
        this.errorMessage = "Sponsor ID not found.";
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:5000/sponsor/ad_request/${sponsorId}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': token,
          },
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to fetch ad requests');
        }

        this.adRequests = data.data;
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    // Handle Edit Action
    editAdRequest(adRequestId) {
      this.$router.push(`/ad_request/${adRequestId}`);
    },
    // Handle Delete Action
    async deleteAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      try {
        const response = await fetch(`http://127.0.0.1:5000/ad_request/${adRequestId}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': token,
          },
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to delete ad request');
        }

        // Directly remove the deleted ad request from the local list
        this.adRequests = this.adRequests.filter(adRequest => adRequest.id !== adRequestId);
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    // Mark the Ad Request as Completed
    async markAsCompleted(adRequestId) {
      const token = localStorage.getItem('authToken');
      try {
        const response = await fetch(`http://127.0.0.1:5000/ad_request/${adRequestId}`, {
          method: 'PUT',
          headers: {
            'Authentication-Token': token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ status: 'Completed' })  // Update the status to 'Completed'
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to mark ad request as completed');
        }

        // Update the ad request status locally
        const adRequest = this.adRequests.find(request => request.id === adRequestId);
        if (adRequest) {
          adRequest.status = 'Completed';
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
  },
};
</script>

<style scoped>
.sponsor-adrequests {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  font-family: 'Arial', sans-serif;
  margin-bottom: 20px;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.no-requests-message {
  text-align: center;
  margin-top: 10px;
  color: #666;
  font-weight: bold;
}

.expired-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}

.adrequest-item {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #fff;
}

.flagged-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}

.completed-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
  margin-top: 10px;
}

.edit-button,
.delete-button,
.complete-button {
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.edit-button {
  background-color: #008bf5;
  color: white;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.complete-button {
  background-color: #0f25ec;
  color: white;
}

.disabled-button {
  background-color: gray;
  cursor: not-allowed;
}

button:hover {
  background-color: #585f5d;
}
</style>
