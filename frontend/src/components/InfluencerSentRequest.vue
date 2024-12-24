<template>
  <div class="influencer-adrequests">
    <h2>Sent Ad Requests</h2>
    <div class="adrequest-cards">
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="!adRequests.length && !errorMessage" class="no-requests-message">No ad requests found.</div>
      <div v-for="adRequest in adRequests" :key="adRequest.id" class="adrequest-card">
        <p><strong>Campaign Name:</strong> {{ adRequest.campaign_name }}</p>
        <p><strong>Sponsor Name:</strong> {{ adRequest.sponsor_name }}</p>
        <p><strong>Message:</strong> {{ adRequest.messages }}</p>
        <p><strong>Requirements:</strong> {{ adRequest.requirements }}</p>
        <p><strong>Acceptance Status:</strong> {{ adRequest.status }}</p>
        <p><strong>Payment Amount:</strong> {{ adRequest.payment_amt }}</p>

        <!-- Display flagged messages -->
        <p v-if="adRequest.campaign_flagged || adRequest.sponsor_flagged" class="flagged-message">The campaign or sponsor is flagged so do not proceed further.</p>
        <!-- <p v-if="adRequest.sponsor_flagged" class="flagged-message">The sponsor is flagged and cannot continue with the campaign.</p> -->

        <div class="button-group">
          <!-- Show Edit button only if status is 'Pending' and campaign/sponsor is not flagged -->
          <button v-if="adRequest.status === 'Pending' && !adRequest.campaign_flagged && !adRequest.sponsor_flagged" @click="editAdRequest(adRequest.id)" class="edit-button">Edit</button>
          <button v-if="adRequest.status === 'Pending' || adRequest.status ==='rejected'" @click="deleteAdRequest(adRequest.id)" class="delete-button">Delete</button>
        </div>

        <p v-if="adRequest.status === 'Completed'" class="completed-message">
          This request has been successfully completed.
        </p>
      </div>
    </div>
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
  const influencerId = localStorage.getItem('influencer_id');

  if (!influencerId) {
    this.errorMessage = "Influencer ID not found.";
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/influencer/ad_request/${influencerId}`, {
      method: 'GET',
      headers: {
        'Authentication-Token': token,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Failed to fetch ad requests');
    }

    console.log('Fetched Ad Requests:', data.data); // Log the entire response data to check flag status

    this.adRequests = data.data;
  } catch (error) {
    this.errorMessage = error.message;
  }
    },
    // Handle Edit Action
    editAdRequest(adRequestId) {
      this.$router.push(`/influencer_specific_ad_request/${adRequestId}`);  // Navigate to the edit ad request page
    },
    // Handle Delete Action
    async deleteAdRequest(adRequestId) {
      const token = localStorage.getItem('authToken');
      try {
        const response = await fetch(`http://127.0.0.1:5000/influencer_specific_ad_request/${adRequestId}`, {
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
  },
};
</script>

<style scoped>
.influencer-adrequests {
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

.adrequest-cards {
  display: flex;
  flex-direction: column; /* Stack items vertically */
}

.adrequest-card {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #fff;
}

.no-requests-message {
  text-align: center;
  margin-top: 10px;
  color: #666;
  font-weight: bold;
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

.button-group {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
  margin-top: 10px;
}

.completed-message {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}

.edit-button,
.delete-button {
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

button:hover {
  background-color: #0056b3;
}
</style>
