<template>
  <div class="received-ad-requests">
    <h2>Received Ad Requests from Influencers</h2>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    <div v-if="!adRequests.length && !errorMessage" class="no-requests-message">No ad requests found.</div>
    <ul>
      <li v-for="request in adRequests" :key="request.id" class="request-item">
        <p><strong>Influencer Name:</strong> {{ request.influencer_name }}</p>
        <p><strong>Campaign:</strong> {{ request.campaign_name }}</p>
        <p><strong>Message:</strong> {{ request.messages }}</p>
        <p><strong>Requirements:</strong> {{ request.requirements }}</p>
        <p><strong>Payment Amount:</strong> {{ request.payment_amt }}</p>
        <p><strong>Influencer Niche:</strong> {{ request.influencer_niche }}</p>
        <p><strong>Influencer Reach:</strong> {{ request.influencer_reach }}</p>
        <p><strong>Influencer Platform:</strong> {{ request.influencer_platform }}</p>
        <p><strong>Status:</strong> {{ request.status }}</p>

        <!-- Show appropriate messages based on the flags and status -->
        <p v-if="request.influencer_flagged && request.status !== 'Completed'" class="flagged-message">
           This influencer is flagged, so do not proceed further.
        </p>
        <p v-if="request.campaign_flagged && request.status !== 'Completed'" class="flagged-message">
           This campaign is flagged, so do not proceed further.
        </p>

        <!-- Disable buttons if the request is flagged or if the status is 'Completed' -->
        <div class="button-group">
          <button 
            v-if="request.status === 'Pending' && !request.influencer_flagged && !request.campaign_flagged" 
            @click="acceptRequest(request.id)" 
            class="accept-button">Accept
          </button>
          <button 
            v-if="request.status === 'Pending' && !request.influencer_flagged && !request.campaign_flagged" 
            @click="rejectRequest(request.id)" 
            class="reject-button">Reject
          </button>

          <!-- Show disabled buttons if flagged or already accepted but flagged -->
          <button 
            v-if="(request.status === 'Pending' || request.status === 'accepted') && (request.influencer_flagged || request.campaign_flagged) && request.status !== 'Completed'" 
            disabled class="disabled-button">Accept
          </button>
          <button 
            v-if="(request.status === 'Pending' || request.status === 'accepted') && (request.influencer_flagged || request.campaign_flagged) && request.status !== 'Completed'" 
            disabled class="disabled-button">Reject
          </button>

          <!-- Show Mark as Completed button if the status is 'Accepted' -->
          <button 
            v-if="request.status === 'accepted' && request.status !== 'Completed' && !request.influencer_flagged && !request.campaign_flagged" 
            @click="markAsCompleted(request.id)" 
            class="complete-button">Mark as Completed
        </button>

        </div>

        <!-- Show completion message if marked as Completed -->
        <p v-if="request.status === 'Completed'" class="completed-message">
          This request has been successfully completed.
        </p>
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
      successMessage: '',
    };
  },
  mounted() {
    this.fetchAdRequests();
  },
  methods: {
    async fetchAdRequests() {
      const token = localStorage.getItem('authToken');
      const sponsorId = localStorage.getItem('sponsor_id');

      try {
        const response = await fetch(`http://127.0.0.1:5000/sponsor/ad_requests/${sponsorId}`, {
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
    async acceptRequest(id) {
      await this.updateRequestStatus(id, 'accept');
    },
    async rejectRequest(id) {
      await this.updateRequestStatus(id, 'reject');
    },
    async markAsCompleted(id) {
      const token = localStorage.getItem('authToken');
      const sponsor_id = localStorage.getItem('sponsor_id');
      try {
        const response = await fetch(`http://127.0.0.1:5000/sponsor/ad_requests/${id}`, {
          method: 'PUT',
          headers: {
            'Authentication-Token': token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ action: 'markAsCompleted', sponsor_id }) 
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to mark ad request as completed');
        }

        // Update the ad request status locally
        const adRequest = this.adRequests.find(request => request.id === id);
        if (adRequest) {
          adRequest.status = 'Completed';
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },

    async updateRequestStatus(id, action) {
      const token = localStorage.getItem('authToken');
      const sponsor_id = localStorage.getItem('sponsor_id');

      try {
        const response = await fetch(`http://127.0.0.1:5000/sponsor/ad_requests/${id}`, {
          method: 'PUT',
          headers: {
            'Authentication-Token': token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ action, sponsor_id }),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || `Failed to ${action} request`);
        }

        this.successMessage = `Ad request ${action}ed successfully!`;
        setTimeout(() => {
          this.successMessage = '';
        }, 2000);

        // Refresh the list of ad requests
        await this.fetchAdRequests();
      } catch (error) {
        this.errorMessage = error.message;
        setTimeout(() => {
          this.errorMessage = '';
        }, 2000);
      }
    },
  },
};
</script>

<style scoped>
.received-ad-requests {
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

.flagged-message {
  color: red;
  font-weight: bold;
}

.success-message {
  color: green;
  text-align: center;
  margin-top: 10px;
}

.no-requests-message {
  text-align: center;
  margin-top: 10px;
  color: #666;
  font-weight: bold;
}

.request-item {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #fff;
}

.button-group {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
  margin-top: 10px;
}

.accept-button, .reject-button, .complete-button, .disabled-button {
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.accept-button {
  background-color: #0336ed;
  color: white;
}

.reject-button {
  background-color: #f44336;
  color: white;
}

.complete-button {
  background-color: #007bff;
  color: white;
}

.disabled-button {
  background-color: gray;
  color: white;
  cursor: not-allowed;
}

.completed-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}
</style>
