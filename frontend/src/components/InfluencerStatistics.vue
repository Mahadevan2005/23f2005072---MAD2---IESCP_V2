<template>
    <div class="influencer-stats">
      <h2>Influencer Statistics</h2>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="!stats && !errorMessage" class="no-stats-message">No statistics available.</div>
  
      <div v-if="stats" class="stats-container">
        <div class="stats-item">
          <div class="stat-label">Total Ad Requests Sent:</div>
          <div class="stat-value">{{ stats.total_adrequest_sent }}</div>
        </div>
  
        <div class="stats-item">
          <div class="stat-label">Total Ad Requests Received:</div>
          <div class="stat-value">{{ stats.total_adrequest_received }}</div>
        </div>
  
        <div class="stats-item">
          <div class="stat-label">Accepted Ad Requests:</div>
          <div class="stat-value">{{ stats.total_adrequest_accepted }}</div>
        </div>
  
        <div class="stats-item">
          <div class="stat-label">Declined Ad Requests:</div>
          <div class="stat-value">{{ stats.total_adrequest_rejected }}</div>
        </div>

        <div class="stats-item">
          <div class="stat-label">Completed Requests:</div>
          <div class="stat-value">{{ stats.total_completed_campaigns }}</div>
        </div>
        
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        stats: null,
        errorMessage: '',
      };
    },
    props: {
      influencerId: {
        type: Number,
        required: true,
      },
    },
    mounted() {
      this.fetchStatistics();
    },
    methods: {
      async fetchStatistics() {
        const token = localStorage.getItem('authToken');
        const influencer_id = localStorage.getItem('influencer_id');
        if (!this.influencerId) {
          this.errorMessage = 'Influencer ID not provided.';
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/influencer/${influencer_id}/statistics`, {
            method: 'GET',
            headers: {
              'Authentication-Token': token,
            },
          });
          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch influencer statistics');
          }
          this.stats = data.data;
        } catch (error) {
          this.errorMessage = error.message;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .influencer-stats {
    max-width: 600px;
    margin: auto;
    padding: 30px;
    border-radius: 12px;
    background-color: #fafafa;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    text-align: center;
    color: #2a9d8f;
    font-family: 'Arial', sans-serif;
    margin-bottom: 30px;
    letter-spacing: 1px;
  }
  
  .stats-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  
  .stats-item {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }
  
  .stat-label {
    font-size: 0.9rem;
    color: #555;
    margin-bottom: 10px;
  }
  
  .stat-value {
    font-size: 1.2rem;
    color: #333;
    font-weight: bold;
  }
  
  .error-message {
    color: red;
    text-align: center;
    margin-top: 10px;
  }
  
  .no-stats-message {
    text-align: center;
    margin-top: 10px;
    color: #999;
    font-weight: bold;
  }
  </style>
  