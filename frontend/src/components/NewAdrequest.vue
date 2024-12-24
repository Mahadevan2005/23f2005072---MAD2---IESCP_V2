<template>
  <div class="new-ad-request">
    <h2>New Ad Request for {{ campaignName }} to {{ influencerName }}</h2>
    <form @submit.prevent="submitAdRequest">
      <div class="form-group">
        <label for="message">Message:</label>
        <textarea id="message" v-model="message" required></textarea>
      </div>
      <div class="form-group">
        <label for="requirements">Requirements:</label>
        <textarea id="requirements" v-model="requirements" required></textarea>
      </div>
      <div class="form-group">
        <label for="payment">Payment Amount:</label>
        <input type="number" id="payment" v-model="payment" required />
      </div>
      <button type="submit" class="submit-button">Send Request</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- Back to Available Influencers button -->
    <button @click="goBack" class="back-button">Back to Available Influencers</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      influencerId: this.$route.params.influencer_id,
      campaignId: this.$route.params.campaign_id,
      campaignName: this.$route.params.campaign_name,
      influencerName: this.$route.params.influencer_name,
      message: '',
      requirements: '',
      payment: null,
      errorMessage: '',
    };
  },
  methods: {
    async submitAdRequest() {
      // Validate payment amount
      if (this.payment <= 0) {
        this.errorMessage = 'Payment amount must be greater than zero.';
        return; // Prevent form submission
      }

      const requestData = {
        influencer_id: this.influencerId,
        campaign_id: this.campaignId,
        message: this.message,
        requirements: this.requirements,
        payment: this.payment,
      };

      const authToken = localStorage.getItem('authToken');
      try {
        // Directly await the axios post request without storing the response
        await axios.post('http://127.0.0.1:5000/sponsor/ad_request', requestData, {
          headers: {
            'Authentication-Token': authToken,
            'Content-Type': 'application/json',
          },
        });
        alert('Ad request sent successfully!');
        this.$router.push('/sponsor_dashboard');
      } catch (error) {
        this.errorMessage = error.response
          ? error.response.data.message
          : 'An error occurred. Please try again.';
      }
    },

    goBack() {
      this.$router.go(-1); // Navigates back to the previous page
    },
  },
};
</script>

<style scoped>
.new-ad-request {
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

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input[type="text"],
input[type="number"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

textarea {
  height: 100px;
  resize: none;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 15px;
}

.back-button {
  width: 100%;
  padding: 10px;
  background-color: #6c757d; /* Grey color for back button */
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 15px;
}

.back-button:hover {
  background-color: #5a6268; /* Darker grey on hover */
}
</style>
