<template>
  <div class="profile-card">
    <div class="profile-header">
      <h2>Profile</h2>
    </div>
    <div class="profile-details">
      <p><strong>Username:</strong> {{ userDetails.username }}</p>
      <p><strong>E-mail:</strong> {{ userDetails.email }}</p>
      <p><strong>Category:</strong> {{ userDetails.category }}</p>
      <p><strong>Niche:</strong> {{ userDetails.niche }}</p>
      <p><strong>Reach:</strong> {{ userDetails.reach }}</p>
      <p><strong>Platform:</strong> {{ userDetails.platform }}</p>
    </div>
    <div class="update-button-container">
      <button @click="updateDetails">Update Details</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userDetails: {},
      errorMessage: '' // Optional: to handle errors
    };
  },
  mounted() {
    this.fetchInfluencerDetails();
  },
  methods: {
    async fetchInfluencerDetails() {
      const token = localStorage.getItem('authToken'); // Fetch token from local storage for authentication
      const influencerId = localStorage.getItem('influencer_id'); // Fetch influencer ID

      try {
        const response = await fetch(`http://127.0.0.1:5000/influencer/profile/${influencerId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': token,
          },
        });

        // Check if the response is okay
        if (!response.ok) {
          throw new Error('Failed to fetch influencer details');
        }

        const data = await response.json(); // Parse JSON response
        this.userDetails = {
          username: data.username,
          email: data.email,
          category: data.category,
          niche: data.niche,
          reach: data.reach,
          platform: data.platform,
        };
      } catch (error) {
        this.errorMessage = error.message; // Handle any errors
      }
    },
    updateDetails() {
      // Logic to handle updating details (e.g., navigating to an update form or opening a modal)
      this.$router.push('/influencer_profile_update');
    },
  },
};
</script>

<style scoped>
.profile-card {
  background-color: #f2e6d9;
  color: #6a4b3a;
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

.update-button-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.update-button-container button {
  background-color: #31572c;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.update-button-container button:hover {
  background-color: #55844c;
}
</style>
