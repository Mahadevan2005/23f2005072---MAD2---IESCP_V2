<template>
    <div class="new-ad-request">
      <h2>New Ad Request for Campaign: {{ campaignName }}</h2>
      <form @submit.prevent="submitAdRequest">
        <div class="form-group">
          <label for="message">Message to Sponsor:</label>
          <textarea id="message" v-model="message" required></textarea>
        </div>
        <div class="form-group">
          <label for="requirements">Proposal or Requirements:</label>
          <textarea id="requirements" v-model="requirements" required></textarea>
        </div>
        <div class="form-group">
          <label for="payment">Proposed Payment Amount:</label>
          <input type="number" id="payment" v-model="payment" required>
        </div>
        <button type="submit" class="submit-button">Send Ad Request</button>
      </form>
  
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
  
      <!-- Back to Available Campaigns button -->
      <button @click="goBack" class="back-button">Back to Campaigns</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        campaignId: this.$route.params.campaign_id,  // Passed from route params
        campaignName: this.$route.params.campaign_name,  // Passed from route params
        influencerId: localStorage.getItem('influencer_id'),  // Influencer ID from storage or session
        message: '',
        requirements: '',
        payment: null,
        errorMessage: '',
        successMessage: '',
      };
    },
    methods: {
      async submitAdRequest() {
        // Validate the proposed payment
        if (this.payment <= 0) {
          this.errorMessage = 'Payment amount must be greater than zero.';
          return;  // Prevent form submission if invalid
        }
  
        const requestData = {
          influencer_id: this.influencerId,
          campaign_id: this.campaignId,
          message: this.message,
          requirements: this.requirements,
          payment: this.payment,
        };
  
        const authToken = localStorage.getItem('authToken');  // Assume influencer is authenticated
  
        try {
          const response = await axios.post('http://127.0.0.1:5000/influencer/ad_request', requestData, {
            headers: {
              'Authentication-Token': authToken,
              'Content-Type': 'application/json',
            },
          });
          if (response.status === 201) {
            this.successMessage = 'Ad request sent successfully!';
            this.errorMessage = '';
          }
        } catch (error) {
          this.errorMessage = error.response
            ? error.response.data.message
            : 'An error occurred. Please try again.';
          this.successMessage = '';
        }
      },
      goBack() {
        this.$router.push('/influencer_dashboard'); // Emit an event to notify parent to show campaigns
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
  
  .success-message {
    color: green;
    text-align: center;
    margin-top: 15px;
  }
  
  .back-button {
    width: 100%;
    padding: 10px;
    background-color: #6c757d;
    color: white;
    border: none;
    border-radius: 4px;
    margin-top: 15px;
    cursor: pointer;
  }
  
  .back-button:hover {
    background-color: #5a6268;
  }
  </style>
  