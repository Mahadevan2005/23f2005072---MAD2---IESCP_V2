<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Admin Dashboard</h1>
      <div class="nav-buttons">
        <button @click="showStats" :class="{ active: showingStats }">App Statistics</button>
        <button @click="showSponsorRequest" :class="{ active: showingSponsorRequest }">Sponsor Requests</button>
        <button @click="showInfluencerRequest" :class="{ active: showingInfluencerRequest }">Influencer Requests</button>
        <button @click="showCampaignRequest" :class="{ active: showingCampaignRequest }">Campaign Requests</button>
        <button @click="logout">Logout</button>
      </div>
    </header>
    <main class="dashboard-content">
      <AdminStats v-if="showingStats" />
      <SponsorRequest v-if="showingSponsorRequest" />
      <InfluencerRequest v-if="showingInfluencerRequest" />
      <CampaignRequest v-if="showingCampaignRequest" />
    </main>
  </div>
</template>

<script>
import SponsorRequest from '@/components/SponsorRequest.vue';
import InfluencerRequest from '@/components/InfluencerRequest.vue';
import CampaignRequest from '@/components/CampaignRequest.vue';
import AdminStats from '@/components/AdminStats.vue';

export default {
  name: 'AdminDashboard',
  components: {
    SponsorRequest,
    InfluencerRequest,
    CampaignRequest,
    AdminStats,
  },
  data() {
    return {
      showingSponsorRequest: false,
      showingInfluencerRequest: false,
      showingCampaignRequest: false,
      showingStats: true,
    };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/admin_login');
    },
    showSponsorRequest() {
      this.showingSponsorRequest = true;
      this.showingInfluencerRequest = false;
      this.showingCampaignRequest = false;
      this.showingStats = false;
    },
    showInfluencerRequest() {
      this.showingSponsorRequest = false;
      this.showingInfluencerRequest = true;
      this.showingCampaignRequest = false;
      this.showingStats = false;
    },
    showCampaignRequest() {
      this.showingSponsorRequest = false;
      this.showingInfluencerRequest = false;
      this.showingCampaignRequest = true;
      this.showingStats = false;
    },
    showStats() {
      this.showingSponsorRequest = false;
      this.showingInfluencerRequest = false;
      this.showingCampaignRequest = false;
      this.showingStats = true;
    },
  },
};
</script>

<style scoped>
.dashboard {
  height: 100vh;
  background-color: #f3f4f6;
  font-family: 'Arial', sans-serif;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #264653;
  color: #ffffff;
  padding: 15px 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
  margin: 0;
  font-size: 1.8rem;
  font-family: 'Roboto', sans-serif;
}

.nav-buttons {
  display: flex;
  gap: 15px;
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

.nav-buttons button.active {
  background-color: #0024ef;
}

.nav-buttons button:hover {
  background-color: #21867a;
}

.dashboard-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}
</style>




<!-- <template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Admin Dashboard</h1>
      <div class="header-buttons">
        <button @click="logout">Logout</button>
      </div>
    </header>
    <div class="dashboard-content">
      <aside class="sidebar">
        <div class="nav-buttons">
          <button @click="showStats" :class="{ active: showingStats }">App Statistics</button> 
          <button @click="showSponsorRequest" :class="{ active: showingSponsorRequest }">Sponsor Requests</button>
          <button @click="showInfluencerRequest" :class="{ active: showingInfluencerRequest }">Influencer Requests</button>
          <button @click="showCampaignRequest" :class="{ active: showingCampaignRequest }">Campaign Requests</button>
        </div>
      </aside>
      <main class="main-content">
        <SponsorRequest v-if="showingSponsorRequest" />
        <InfluencerRequest v-if="showingInfluencerRequest" />
        <CampaignRequest v-if="showingCampaignRequest" />
        <AdminStats v-if="showingStats" /> 
      </main>
    </div>
  </div>
</template>

<script>
import SponsorRequest from '@/components/SponsorRequest.vue';
import InfluencerRequest from '@/components/InfluencerRequest.vue';
import CampaignRequest from '@/components/CampaignRequest.vue';  
import AdminStats from '@/components/AdminStats.vue'; // Import AdminStats component

export default {
  name: 'AdminDashboard',
  components: {
    SponsorRequest,
    InfluencerRequest,
    CampaignRequest,  
    AdminStats, // Register AdminStats component
  },
  data() {
    return {
      showingSponsorRequest: false,
      showingInfluencerRequest: false,
      showingCampaignRequest: false,
      showingStats: true, // New data property to track statistics display
    };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/admin_login');
    },
    showSponsorRequest() {
      this.showingSponsorRequest = true;
      this.showingInfluencerRequest = false;
      this.showingCampaignRequest = false;
      this.showingStats = false; // Hide stats when showing other requests
    },
    showInfluencerRequest() {
      this.showingSponsorRequest = false;
      this.showingInfluencerRequest = true;
      this.showingCampaignRequest = false;
      this.showingStats = false; // Hide stats when showing other requests
    },
    showCampaignRequest() {
      this.showingSponsorRequest = false;
      this.showingInfluencerRequest = false;
      this.showingCampaignRequest = true;
      this.showingStats = false; // Hide stats when showing other requests
    },
    showStats() {
      this.showingSponsorRequest = false;
      this.showingInfluencerRequest = false;
      this.showingCampaignRequest = false;
      this.showingStats = true; // Show stats
    },
  },
};
</script>

<style scoped>
/* Styles remain the same */
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f3f4f6;
  font-family: 'Arial', sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background-color: #264653;
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
  margin: 0;
  font-size: 1.8rem;
  font-family: 'Roboto', sans-serif;
  letter-spacing: 1px;
}

.header-buttons button {
  background-color: #2a9d8f;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.header-buttons button:hover {
  background-color: #21867a;
}

.dashboard-content {
  display: flex;
  flex: 1;
  margin-top: 10px;
}

.sidebar {
  width: 220px;
  background-color: #2a9d8f;
  padding: 25px;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h2 {
  margin-bottom: 15px;
  color: #ffffff;
}

.nav-buttons {
  display: flex;
  flex-direction: column;
}

.nav-buttons button {
  background-color: #264653;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 15px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease, transform 0.1s ease;
}

.nav-buttons button.active {
  background-color: #0024ef; /* Active button color */
}

.nav-buttons button:hover {
  background-color: #1e3d47;
  transform: translateY(-2px);
}

.main-content {
  flex: 1;
  padding: 30px;
  background-color: #ffffff;
  border-left: 2px solid #e0e0e0;
  overflow-y: auto;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05);
}
</style> -->