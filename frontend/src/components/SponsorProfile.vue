<template>
    <div class="profile-card">
      <div class="profile-header">
        <h2>Profile</h2>
      </div>
      <div class="profile-details">
        <p><strong>Username:</strong> {{ sponsorDetails.username }}</p>
        <p><strong>E-mail:</strong> {{ sponsorDetails.email }}</p>
        <p><strong>Industry:</strong> {{ sponsorDetails.industry }}</p>
        <p><strong>Company Name:</strong> {{ sponsorDetails.company_name }}</p>
        <p><strong>Company Budget:</strong> {{ sponsorDetails.company_budget }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sponsorDetails: {}, 
        errorMessage: '', 
      };
    },
    mounted() {
      this.fetchSponsorDetails(); // Fetch sponsor details when component mounts
    },
    methods: {
      async fetchSponsorDetails() {
        const token = localStorage.getItem('authToken'); // Fetch token from local storage for authentication
        const sponsorId = localStorage.getItem('sponsor_id'); // Fetch sponsor ID
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/sponsor/details/${sponsorId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': token,
            },
          });
  
          // Check if the response is okay
          if (!response.ok) {
            throw new Error('Failed to fetch sponsor details');
          }
  
          const data = await response.json(); // Parse JSON response
          this.sponsorDetails = {
            company_name: data.company_name,
            company_budget: data.company_budget,
            username: data.username,
            email: data.email,
            industry: data.industry,
            flagged: data.flagged,
            approved: data.approved,
          };
        } catch (error) {
          this.errorMessage = error.message; // Handle any errors
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .profile-card {
    background-color: #f2e6d9; /* Light background for sponsor profile */
    color: #6a4b3a; /* Dark text color for contrast */
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .profile-header {
    display: flex;
    align-items: center;
  }
  
  .profile-details {
    margin-top: 10px;
  }
  </style>
  