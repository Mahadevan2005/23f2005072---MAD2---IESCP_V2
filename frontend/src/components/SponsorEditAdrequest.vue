<template>
    <div class="edit-adrequest">
      <h2>Edit Ad Request</h2>
      <form @submit.prevent="updateAdRequest">
        <div class="form-group">
          <label for="messages">Message:</label>
          <textarea id="messages" v-model="adRequest.messages" required></textarea>
        </div>
        <div class="form-group">
          <label for="requirements">Requirements:</label>
          <textarea id="requirements" v-model="adRequest.requirements" required></textarea>
        </div>
        <div class="form-group">
          <label for="payment_amt">Payment Amount:</label>
          <input type="number" id="payment_amt" v-model="adRequest.payment_amt" required />
        </div>
        <button type="submit" class="submit-button">Update Ad Request</button>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      </form>
      <button class="back-button" @click="goBack">Back</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        adRequest: {
          messages: '',
          requirements: '',
          payment_amt: ''
        },
        errorMessage: '',
        successMessage: '',
      };
    },
    mounted() {
      this.fetchAdRequest();
    },
    methods: {
      async fetchAdRequest() {
        const token = localStorage.getItem('authToken');
        const adRequestId = this.$route.params.id; // Assuming your route parameter for the ad request ID is named 'id'
        try {
          const response = await fetch(`http://127.0.0.1:5000/ad_request/${adRequestId}`, {
            method: 'GET',
            headers: {
              'Authentication-Token': token,
            },
          });
  
          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch ad request');
          }
  
          this.adRequest = data.data; // Assuming the response has the data field with the ad request details
        } catch (error) {
          this.errorMessage = error.message;
          setTimeout(() => {
            this.errorMessage = '';
          }, 1000); // Clear error message after 1 second
        }
      },
      async updateAdRequest() {
        const token = localStorage.getItem('authToken');
        const adRequestId = this.$route.params.id; // Assuming your route parameter for the ad request ID is named 'id'

        // Validate payment amount
        if (this.adRequest.payment_amt <= 0) {
          this.errorMessage = "Payment amount must be greater than 0.";
          setTimeout(() => {
            this.errorMessage = '';
          }, 1000); // Clear error message after 1 second
          return; // Prevent the API call
        }

        try {
          const response = await fetch(`http://127.0.0.1:5000/ad_request/${adRequestId}`, {
            method: 'PUT',
            headers: {
              'Authentication-Token': token,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.adRequest)
          });

          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.message || 'Failed to update ad request');
          }

          this.successMessage = "Ad request updated successfully!";
          setTimeout(() => {
            this.successMessage = '';
            this.goBack(); // Optionally navigate back after success
          }, 2000); // Clear success message after 2 seconds
        } catch (error) {
          this.errorMessage = error.message;
          setTimeout(() => {
            this.errorMessage = '';
          }, 2000); // Clear error message after 2 seconds
        }
      },
      goBack() {
      this.$router.push('/sponsor_dashboard?view=adRequests');
    },
    },
  };
  </script>
  
  <style scoped>
  .edit-adrequest {
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
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
  }
  
  textarea,
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s;
  }
  
  textarea:focus,
  input:focus {
    border-color: #007BFF;
    outline: none;
  }
  
  button.submit-button {
    width: 100%;
    padding: 10px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button.submit-button:hover {
    background-color: #0056b3;
  }
  
  button.back-button {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 10px; /* Space below the button */
  }
  
  button.back-button:hover {
    background-color: #0056b3;
  }
  </style>
  