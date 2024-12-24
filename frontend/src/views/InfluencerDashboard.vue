<template>
  <div class="dashboard">
    <header class="navbar">
      <h1>Influencer's Dashboard</h1>
      <div class="nav-buttons">
        <button @click="showProfile" :class="{ active: showingProfile }">Profile</button>
        <button @click="showStats" :class="{ active: showingStats }">My Statistics</button>
        <button @click="showAllCampaigns" :class="{ active: showingAllCampaigns }">All Campaigns</button>
        <button @click="showSentAdRequests" :class="{ active: showingSentAdRequests }">Sent Ad Requests</button>
        <button @click="showReceivedAdRequests" :class="{ active: showingReceivedAdRequests }">Received Ad Requests</button>
        <button @click="logout">Logout</button>
      </div>
    </header>
    <div class="main-content">
      <InfluencerProfile v-if="showingProfile" />
      <InfluencerStatistics v-if="showingStats" :influencerId="influencerId" />
      <InfluencerAllCampaigns v-if="showingAllCampaigns" />
      <InfluencerSentAdRequests v-if="showingSentAdRequests" />
      <InfluencerReceivedAdRequest v-if="showingReceivedAdRequests" />
    </div>
  </div>
</template>

<script>
import InfluencerProfile from '@/components/InfluencerProfile.vue';
import InfluencerStatistics from '@/components/InfluencerStatistics.vue';
import InfluencerAllCampaigns from '@/components/InfluencerAllCampaigns.vue';
import InfluencerSentAdRequests from '@/components/InfluencerSentRequest.vue';
import InfluencerReceivedAdRequest from '@/components/InfluencerReceivedAdrequest.vue';

export default {
  components: {
    InfluencerProfile,
    InfluencerStatistics,
    InfluencerAllCampaigns,
    InfluencerSentAdRequests,
    InfluencerReceivedAdRequest,
  },
  data() {
    return {
      influencerId: localStorage.getItem('influencer_id'),
      showingProfile: false,
      showingStats: false,
      showingAllCampaigns: false,
      showingSentAdRequests: false,
      showingReceivedAdRequests: false,
    };
  },
  mounted() {
    const view = this.$route.query.view;
    if (view === 'adRequests') {
      this.showSentAdRequests();
    } else if (view === 'allCampaigns') {
      this.showAllCampaigns();
    } else if (view === 'stats') {
      this.showStats();
    } else {
      this.showProfile();
    }
  },
  methods: {
    showProfile() {
      this.resetViews();
      this.showingProfile = true;
    },
    showStats() {
      this.resetViews();
      this.showingStats = true;
    },
    showAllCampaigns() {
      this.resetViews();
      this.showingAllCampaigns = true;
    },
    showSentAdRequests() {
      this.resetViews();
      this.showingSentAdRequests = true;
    },
    showReceivedAdRequests() {
      this.resetViews();
      this.showingReceivedAdRequests = true;
    },
    resetViews() {
      this.showingProfile = false;
      this.showingStats = false;
      this.showingAllCampaigns = false;
      this.showingSentAdRequests = false;
      this.showingReceivedAdRequests = false;
    },
    logout() {
      localStorage.clear();
      this.$router.push('/influencer_login');
    },
  },
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f3f4f6;
  font-family: 'Arial', sans-serif;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background-color: #264653;
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar h1 {
  font-size: 1.5rem;
  margin-right: 20px;
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.nav-buttons button {
  background-color: #2a9d8f;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.nav-buttons button:hover {
  background-color: #21867a;
}

.nav-buttons button.active {
  background-color: #1e3d47;
}

.main-content {
  flex: 1;
  padding: 30px;
  background-color: #ffffff;
  overflow-y: auto;
}
</style>
