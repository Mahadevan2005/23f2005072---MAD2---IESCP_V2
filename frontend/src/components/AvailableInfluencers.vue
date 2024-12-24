<template>
  <div class="available-influencers">
    <button @click="goBack" class="back-button">Back</button>
    <h2>Available Influencers for "{{ campaignName }}"</h2>

    <!-- Search Input and Button -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by niche, industry, platform, or name"
        class="search-input"
      />
      <button @click="searchInfluencers" class="search-button">Search</button>
    </div>

    <!-- Display error message if any -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>


    <!-- Display the influencer cards or no results message -->
    <div v-if="!loading && !errorMessage">
      <div v-if="searchActive && !filteredInfluencers.length" class="no-results-message">
        No influencers found matching your search.
      </div>
      <div v-else-if="!searchActive && !influencers.length" class="no-results-message">
        No influencers available.
      </div>
      <div class="influencer-cards" v-if="(searchActive && filteredInfluencers.length) || (!searchActive && influencers.length)">
        <div 
          v-for="influencer in (searchActive && filteredInfluencers.length ? filteredInfluencers : influencers)" 
          :key="influencer.influencer_id" 
          class="influencer-card"
        >
          <h3>{{ influencer.name }}</h3>
          <p><strong>Category:</strong> {{ influencer.category }}</p>
          <p><strong>Reach:</strong> {{ influencer.reach }}</p>
          <p><strong>Niche:</strong> {{ influencer.niche }}</p>
          <p><strong>Platform:</strong> {{ influencer.platform }}</p>
          <button @click="requestInfluencer(influencer)" class="request-button">Request</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      influencers: [],            // Store all influencers
      filteredInfluencers: [],    // Store search results
      searchQuery: '',            // Search query
      errorMessage: '',           // For error messages
      searchActive: false,        // To track if search was made
      loading: false,             // For loading state
      campaignName: this.$route.params.campaignName,  // Campaign name from route
    };
  },
  mounted() {
    this.fetchInfluencers(); // Fetch influencers on mount
  },
  methods: {
    async fetchInfluencers() {
      const token = localStorage.getItem('authToken');
      this.loading = true; // Set loading state
      try {
        const response = await fetch('http://127.0.0.1:5000/all_active/influencers', {
          method: 'GET',
          headers: {
            'Authentication-Token': token,
          },
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to fetch influencers');
        }

        this.influencers = data.data;  // Store influencers
        this.filteredInfluencers = data.data;  // Initialize filtered influencers
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.loading = false; // Reset loading state
      }
    },

    async searchInfluencers() {
      const token = localStorage.getItem('authToken');
      this.searchActive = true;  // Set search as active
      this.loading = true; // Set loading state
      try {
        // If the search query is empty, set filteredInfluencers to the full list
        if (this.searchQuery.trim() === '') {
          this.filteredInfluencers = this.influencers; // Show all influencers
        } else {
          const response = await fetch(`http://127.0.0.1:5000/search/influencers?query=${this.searchQuery}`, {
            method: 'GET',
            headers: {
              'Authentication-Token': token,
            },
          });

          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.message || 'Failed to search influencers');
          }

          this.filteredInfluencers = data.data;  // Update with search results
        }
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.loading = false; // Reset loading state
      }
    },

    goBack() {
      this.$router.push('/sponsor_dashboard?view=allCampaigns');
    },

    requestInfluencer(influencer) {
      const influencerId = influencer.influencer_id;
      const campaignId = this.$route.params.campaignId;
      this.$router.push({
        name: 'NewAdrequest',
        params: {
          influencer_id: influencerId,
          campaign_id: campaignId,
          campaign_name: this.campaignName,
          influencer_name: influencer.name
        },
      });
    },
  },
};
</script>

<style scoped>
.available-influencers {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

h2 {
  text-align: center;
  color: #333;
  font-family: 'Arial', sans-serif;
  margin-bottom: 20px;
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
  display: inline-block;
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
}

.search-button:hover {
  background-color: #0056b3;
}

.influencer-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.influencer-card {
  background-color: #f4f4f4;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  width: 250px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}


.error-message {
  color: red;
  font-weight: bold;
  text-align: center;
  margin: 20px 0;
}

.loading-message {
  text-align: center;
  margin: 20px 0;
  font-style: italic;
}

.no-results-message {
  text-align: center;
  margin: 20px 0;
  font-style: italic;
  color: #666;
}

.back-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
  display: block;
}

.back-button:hover {
  background-color: #0056b3;
}

.request-button {
  background-color: #0a98ea;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  display: inline-block;
}

.request-button:hover {
  background-color: #218838;
}
</style>
