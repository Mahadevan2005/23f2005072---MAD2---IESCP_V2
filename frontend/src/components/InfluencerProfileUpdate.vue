<template>
    <div class="edit-profile">
      <br>
      <button @click="goToDashboard" class="back-button">Back to Dashboard</button>
      <h2>Edit Profile</h2>
  
      <div v-if="profile.flagged === 1" class="flagged-message">
        Your profile is flagged and cannot be edited.
      </div>
  
      <form @submit.prevent="submitEdit" v-if="profile.flagged !== 1">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="profile.username" disabled>
        </div>
  
        <div class="form-group">
          <label for="category">Category:</label>
          <input type="text" id="category" v-model="profile.category" required :disabled="profile.flagged === 1">
        </div>
  
        <div class="form-group">
          <label for="niche">Niche:</label>
          <input type="text" id="niche" v-model="profile.niche" :disabled="profile.flagged === 1">
        </div>
  
        <div class="form-group">
          <label for="reach">Reach:</label>
          <input type="number" id="reach" v-model="profile.reach" required :disabled="profile.flagged === 1">
        </div>
  
        <div class="form-group">
          <label for="platform">Platform:</label>
          <input type="text" id="platform" v-model="profile.platform" required :disabled="profile.flagged === 1">
        </div>
  
        <button type="submit" class="submit-button" :disabled="profile.flagged === 1">Save Changes</button>
      </form>
  
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        profile: {
          username: '',
          category: '',
          niche: '',
          reach: 0,
          platform: '', // Added platform field
          flagged: 0, // Profile is not flagged initially
        },
        errorMessage: '',
        successMessage: '',
      };
    },
    mounted() {
      this.fetchProfile();
    },
    methods: {
      async fetchProfile() {
        const token = localStorage.getItem('authToken');
        const influencerId = localStorage.getItem('influencer_id');
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/influencer/profile/${influencerId}`, {
            method: 'GET',
            headers: {
              'Authentication-Token': token,
            },
          });
  
          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch profile');
          }
  
          this.profile = {
            username: data.username,
            category: data.category,
            niche: data.niche,
            reach: data.reach,
            platform: data.platform, // Ensure 'platform' exists in the response
            flagged: data.flagged, // Ensure 'flagged' exists in the response
          };
        } catch (error) {
          this.errorMessage = error.message;
        }
      },
      async submitEdit() {
        const token = localStorage.getItem('authToken');
        const influencerId = localStorage.getItem('influencer_id');
  
        // Validation for reach
        if (this.profile.reach <= 0) {
          this.errorMessage = 'Reach must be greater than 0.';
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/influencer/update_details/${influencerId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': token,
            },
            body: JSON.stringify({
              category: this.profile.category,
              niche: this.profile.niche,
              reach: this.profile.reach,
              platform: this.profile.platform, // Include platform in the update
            }),
          });
  
          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.message || 'Failed to update profile');
          }
  
          this.successMessage = 'Profile updated successfully!';
          this.errorMessage = '';
          setTimeout(() => {
            this.successMessage = '';
          }, 3000);
        } catch (error) {
          this.errorMessage = error.message;
        }
      },
      goToDashboard() {
        this.$router.push('/influencer_dashboard');
      },
    },
  };
  </script>
  
  <style scoped>
  .edit-profile {
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
  
  input[type='text'],
  input[type='number'] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s;
  }
  
  input[type='text']:focus,
  input[type='number']:focus {
    border-color: #007BFF;
    outline: none;
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
    transition: background-color 0.3s;
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
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-bottom: 20px;
  }
  
  .back-button:hover {
    background-color: #0056b3;
  }
  
  .flagged-message {
    color: red;
    text-align: center;
    margin-bottom: 15px;
  }
  </style>
  