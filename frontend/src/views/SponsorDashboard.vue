<template>
  <div class="dashboard">
    <header class="navbar">
      <h1>Sponsor's Dashboard</h1>
      <div class="nav-buttons">
        <button @click="showProfile" :class="{ active: showingProfile }">Profile</button>
        <button @click="showStats" :class="{ active: showingStats }">My Statistics</button>
        <button @click="showAllCampaigns" :class="{ active: showingAllCampaigns }">My Campaigns</button>
        <button @click="showAdRequests" :class="{ active: showingAdRequests }">Sent Ad Requests</button>
        <button @click="showReceivedAdrequest" :class="{ active: showingReceivedAdrequest }">Received Ad Requests</button>
        <button @click="showAddCampaign" :class="{ active: showingAddCampaign }">Create New Campaign</button>
        <button @click="create_csv">Download Report</button>
        <button @click="logout">Logout</button>
      </div>
    </header>
    <div class="main-content">
      <SponsorProfile v-if="showingProfile" />
      <SponsorStats v-if="showingStats" :sponsorId="sponsorId" />
      <AddCampaign v-if="showingAddCampaign" />
      <AllCampaigns v-if="showingAllCampaigns" />
      <SponsorAdRequest v-if="showingAdRequests" />
      <SponsorReceivedAdrequest v-if="showingReceivedAdrequest" />
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import AddCampaign from '@/components/NewCampaign.vue';
import AllCampaigns from '@/components/AllCampaigns.vue';
import SponsorAdRequest from '@/components/SponsorAdRequest.vue';
import SponsorReceivedAdrequest from '@/components/SponsorReceivedAdrequest.vue';
import SponsorProfile from '@/components/SponsorProfile.vue';
import SponsorStats from '@/components/SponsorStatistics.vue';

export default {
  components: {
    AddCampaign,
    AllCampaigns,
    SponsorAdRequest,
    SponsorReceivedAdrequest,
    SponsorProfile,
    SponsorStats,
  },
  data() {
    return {
      sponsorId: localStorage.getItem('sponsor_id'),
      showingProfile: false,
      showingStats: false,
      showingAddCampaign: false,
      showingAllCampaigns: false,
      showingAdRequests: false,
      showingReceivedAdrequest: false,
    };
  },
  mounted() {
    const view = this.$route.query.view;
    if (view === 'adRequests') {
      this.showAdRequests();
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
    showAddCampaign() {
      this.resetViews();
      this.showingAddCampaign = true;
    },
    showAllCampaigns() {
      this.resetViews();
      this.showingAllCampaigns = true;
    },
    showAdRequests() {
      this.resetViews();
      this.showingAdRequests = true;
    },
    showReceivedAdrequest() {
      this.resetViews();
      this.showingReceivedAdrequest = true;
    },
    resetViews() {
      this.showingProfile = false;
      this.showingStats = false;
      this.showingAddCampaign = false;
      this.showingAllCampaigns = false;
      this.showingAdRequests = false;
      this.showingReceivedAdrequest = false;
    },
    async create_csv() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/export_csv', {
          params: { sponsor_id: this.sponsorId },
        });
        const { task_id } = res.data; // Accessing task_id correctly
        console.log('Task ID:', task_id);
        alert('Report generation initiated. Please wait...');

        const interval = setInterval(async () => {
          try {
            const res = await axios.get(`http://127.0.0.1:5000/get-csv/${task_id}`);
            if (res.status === 200) {
              console.log("Data is ready");
              window.open(`http://127.0.0.1:5000/get-csv/${task_id}`);
              clearInterval(interval);
            } else {
              console.log('CSV not ready yet. Checking again...');
            }
          } catch (error) {
            console.error('Error fetching CSV status', error);
            clearInterval(interval);
          }
        }, 1000); // Poll every 1000 ms (1 second)
      } catch (error) {
        console.error('Error generating report', error);
        alert('Failed to generate report. Please try again later.');
      }
    },
    logout() {
      localStorage.clear();
      this.$router.push('/sponsor_login');
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



<!-- <template>
  <div class="dashboard">
    <div class="header">
      <h1>Sponsor's Dashboard</h1>
      <div class="header-buttons">
        <button @click="logout">Logout</button>
      </div>
    </div>
    <div class="dashboard-content">
      <div class="sidebar">
        <div class="nav-buttons">
          <button @click="showProfile">Profile</button> <br>
          <button @click="showStats">My Statistics</button>
          <button @click="showAllCampaigns">My Campaigns</button>
          <button @click="showAdRequests">Sent Ad Requests</button>
          <button @click="showReceivedAdrequest">Received Ad Requests</button>
          <button @click="showAddCampaign">Create New Campaign</button>
          <button @click="create_csv">Click to Download Report</button>
        </div>
      </div>
      <div class="main-content">
        <SponsorProfile v-if="showingProfile" />
        <SponsorStats v-if="showingStats" :sponsorId="sponsorId" />
        <AddCampaign v-if="showingAddCampaign" />
        <AllCampaigns v-if="showingAllCampaigns" />
        <SponsorAdRequest v-if="showingAdRequests" />
        <SponsorReceivedAdrequest v-if="showingReceivedAdrequest" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AddCampaign from '@/components/NewCampaign.vue';
import AllCampaigns from '@/components/AllCampaigns.vue';
import SponsorAdRequest from '@/components/SponsorAdRequest.vue';
import SponsorReceivedAdrequest from '@/components/SponsorReceivedAdrequest.vue';
import SponsorProfile from '@/components/SponsorProfile.vue';
import SponsorStats from '@/components/SponsorStatistics.vue';

export default {
  components: {
    AddCampaign,
    AllCampaigns,
    SponsorAdRequest,
    SponsorReceivedAdrequest,
    SponsorProfile,
    SponsorStats,
  },
  data() {
    return {
      sponsorId: localStorage.getItem('sponsor_id'),
      showingProfile: false,
      showingStats: false,
      showingAddCampaign: false,
      showingAllCampaigns: false,
      showingAdRequests: false,
      showingReceivedAdrequest: false,
    };
  },
  mounted() {
    const view = this.$route.query.view;
    if (view === 'adRequests') {
      this.showAdRequests();
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
    showAddCampaign() {
      this.resetViews();
      this.showingAddCampaign = true;
    },
    showAllCampaigns() {
      this.resetViews();
      this.showingAllCampaigns = true;
    },
    showAdRequests() {
      this.resetViews();
      this.showingAdRequests = true;
    },
    showReceivedAdrequest() {
      this.resetViews();
      this.showingReceivedAdrequest = true;
    },
    resetViews() {
      this.showingProfile = false;
      this.showingStats = false;
      this.showingAddCampaign = false;
      this.showingAllCampaigns = false;
      this.showingAdRequests = false;
      this.showingReceivedAdrequest = false;
    },
    async create_csv() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/export_csv', {
          params: { sponsor_id: this.sponsorId },
        });
        const { task_id } = res.data; // Accessing task_id correctly
        console.log('Task ID:', task_id);
        alert('Report generation initiated. Please wait...');

        const interval = setInterval(async () => {
          try {
            const res = await axios.get(http://127.0.0.1:5000/get-csv/${task_id});
            if (res.status === 200) {
              console.log("Data is ready");
              window.open(http://127.0.0.1:5000/get-csv/${task_id});
              clearInterval(interval);
            } else {
              console.log('CSV not ready yet. Checking again...');
            }
          } catch (error) {
            console.error('Error fetching CSV status', error);
            clearInterval(interval);
          }
        }, 1000); // Poll every 1000 ms (1 second)
      } catch (error) {
        console.error('Error generating report', error);
        alert('Failed to generate report. Please try again later.');
      }
    },
    logout() {
      localStorage.clear();
      this.$router.push('/sponsor_login');
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background-color: #264653;
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header h1 {
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