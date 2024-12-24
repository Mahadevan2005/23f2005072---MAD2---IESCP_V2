<template>
  <div class="received-ad-requests">
    <h2>Received Ad Requests from Sponsors</h2>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

    <ul>
      <li v-for="request in adRequests" :key="request.id" class="request-item">
      <p><strong>Sponsor Name:</strong> {{ request.sponsor_name }}</p>
      <p><strong>Campaign:</strong> {{ request.campaign_name }}</p>
      <p><strong>Message:</strong> {{ request.messages }}</p>
      <p><strong>Requirements:</strong> {{ request.requirements }}</p>
      <p><strong>Payment Amount:</strong> {{ request.payment_amt }}</p>
      <p><strong>Start Date:</strong> {{ formatDate(request.start_date) }}</p>
      <p><strong>End Date:</strong> {{ formatDate(request.end_date) }}</p>
      <p><strong>Status:</strong> {{ request.status }}</p>

      <p v-if="request.is_expired" class="expired-message">
        The campaign has expired and no further action can be taken.
      </p>


        <!-- <p v-if="request.campaign_flagged === 1 && request.sponsor_flagged === 1  && request.status !== 'Completed'" class="flagged-message">
          This sponsor (or) campaign is flagged and cannot proceed further.
        </p> -->

        <!-- Show message if the campaign or sponsor is flagged -->
        <p v-if="(request.campaign_flagged === 1 || request.sponsor_flagged === 1 )&& request.status !== 'Completed'" class="flagged-message">
          The campaign or sponsor is flagged and cannot proceed further.
        </p>

        <!-- Conditionally render buttons only if status is 'Pending', campaign is not flagged, and sponsor is not flagged -->
        <div v-if="request.status === 'Pending' && request.campaign_flagged === 0 && request.sponsor_flagged === 0 && !request.is_expired">
          <button @click="acceptRequest(request.id)">Accept</button>
          <button @click="rejectRequest(request.id)">Reject</button>
        </div>

        <!-- If campaign or sponsor is flagged, disable the buttons -->
        <div 
          v-if="(request.campaign_flagged === 1 || request.sponsor_flagged === 1 || request.is_expired) && request.status !== 'Completed'" 
          class="disabled-buttons">
          <button disabled>Accept</button>
          <button disabled>Reject</button>
        </div>

        <!-- Show completed message if status is 'Completed' -->
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
      const influencer_id = localStorage.getItem('influencer_id');
      try {
        const response = await fetch(`http://127.0.0.1:5000/influencer/ad_requests/${influencer_id}`, {
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
        setTimeout(() => {
          this.errorMessage = '';
        }, 2000); // Clear error message after 2 seconds
      }
    },
    async acceptRequest(id) {
      await this.updateRequestStatus(id, 'accept');
    },
    async rejectRequest(id) {
      await this.updateRequestStatus(id, 'reject');
    },
    async updateRequestStatus(id, action) {
      const token = localStorage.getItem('authToken');
      const influencer_id = localStorage.getItem('influencer_id');  // Get influencer_id from local storage

      try {
        const response = await fetch(`http://127.0.0.1:5000/influencer/ad_requests/${id}`, {
          method: 'PUT',
          headers: {
            'Authentication-Token': token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ action, influencer_id })  
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || `Failed to ${action} request`);
        }

        this.successMessage = `Ad request ${action}ed successfully!`;
        setTimeout(() => {
          this.successMessage = '';
        }, 2000); // Clear success message after 2 seconds

        // Refresh the list of ad requests
        await this.fetchAdRequests();
      } catch (error) {
        this.errorMessage = error.message;
        setTimeout(() => {
          this.errorMessage = '';
        }, 2000); // Clear error message after 2 seconds
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'; // Handle null or undefined dates
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
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

.success-message {
  color: green;
  text-align: center;
  margin-top: 10px;
}

.request-item {
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

.expired-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}

button {
  margin-right: 10px;
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}

.disabled-buttons button {
  background-color: gray;
  cursor: not-allowed;
}

.completed-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}
</style>
