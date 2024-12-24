<template>
  <div>
    <h2>Public Campaigns</h2>
    
    
    <!-- Search Input and Button -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by campaign name, description, goals, or niche"
        class="search-input"
      />
      <button @click="searchCampaigns" class="search-button">Search</button>
    </div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <div v-if="!errorMessage">
      <div v-for="campaign in (searchActive && filteredCampaigns.length ? filteredCampaigns : campaigns)" 
           :key="campaign.campaign_id" 
           class="campaign-card">
        <h3>{{ campaign.name }}</h3>
        <p><strong>Sponsor Name:</strong> {{ campaign.sponsor_name }}</p>
        <p><strong>Description:</strong> {{ campaign.description }}</p>
        <p><strong>Niche:</strong> {{ campaign.niche }}</p>
        <p><strong>Start Date:</strong> {{ campaign.start_date }}</p>
        <p><strong>End Date:</strong> {{ campaign.end_date }}</p>
        <p><strong>Budget:</strong> {{ campaign.campaign_budget }}</p>
        <p><strong>Visibility:</strong> {{ campaign.visibility }}</p>
        <p><strong>Goals:</strong> {{ campaign.goals }}</p>
        <button @click="sendAdRequest(campaign)" class="ad-request-button">Send Ad Request</button>
      </div>

      <!-- No results message -->
      <div v-if="searchActive && !filteredCampaigns.length" class="no-results-message">
        No campaigns found matching your search.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      campaigns: [],                // Store all campaigns
      filteredCampaigns: [],        // Store search results
      searchQuery: '',              // Search query
      errorMessage: '',             // For error messages
      searchActive: false,          // To track if search was made
      loading: false,               // For loading state
    };
  },
  mounted() {
    this.fetchCampaigns(); // Fetch campaigns on mount
  },
  methods: {
    async fetchCampaigns() {
      this.loading = true; // Set loading state
      try {
        const response = await fetch('http://127.0.0.1:5000/all_public_campaigns', {
          method: 'GET',
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to fetch campaigns');
        }

        this.campaigns = data.data;  // Store campaigns
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.loading = false; // Reset loading state
      }
    },

    async searchCampaigns() {
      this.searchActive = true;  // Set search as active
      this.loading = true; // Set loading state
      try {
        const response = await fetch(`http://127.0.0.1:5000/search/campaigns?query=${this.searchQuery}`, {
          method: 'GET',
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to search campaigns');
        }

        this.filteredCampaigns = data.data;  // Update with search results
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.loading = false; // Reset loading state
      }
    },

    // Navigate to the influencer ad request form
    sendAdRequest(campaign) {
      this.$router.push({
        name: 'InfluencerNewAdrequest',  // Route name of the ad request form component
        params: {
          campaign_id: campaign.campaign_id,  // Passing campaign ID
          campaign_name: campaign.name       // Passing campaign name
        }
      });
    },
  },
};
</script>

<style scoped>
.campaign-card {
  background-color: #f4f4f4;
  padding: 20px;
  margin: 10px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.error {
  color: red;
  font-weight: bold;
}

.loading-message {
  text-align: center;
  font-style: italic;
}

.no-results-message {
  text-align: center;
  color: #666;
  font-style: italic;
}

.search-bar {
  text-align: center;
  margin-bottom: 20px;
}

.search-input {
  width: 60%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-button {
  padding: 10px 20px;
  font-size: 16px;
  margin-left: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s; /* Smooth transition for hover effects */
}

.search-button:hover {
  background-color: #0056b3;
  transform: scale(1.05); /* Slightly enlarge button on hover */
}

.ad-request-button {
  background-color: #1b63d7; /* Green color for the Ad Request button */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s; /* Smooth transition for hover effects */
}

.ad-request-button:hover {
  background-color: #218838; /* Darker green on hover */
  transform: scale(1.05); /* Slightly enlarge button on hover */
}
</style>
