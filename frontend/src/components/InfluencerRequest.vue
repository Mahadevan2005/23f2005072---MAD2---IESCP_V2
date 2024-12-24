<template>
  <div>
    <h2>Influencer Requests</h2>
    <table class="influencer-table">
      <thead>
        <tr>
          <th>Influencer Name</th>
          <th>E-mail</th>
          <th>Category</th>
          <th>Reach</th>
          <th>Niche</th>
          <th>Platform</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="influencer in influencers" :key="influencer.influencer_id" class="influencer-row">
          <td>{{ influencer.name }}</td>
          <td>{{ influencer.email }}</td>
          <td>{{ influencer.category }}</td>
          <td>{{ influencer.reach }}</td>
          <td>{{ influencer.niche }}</td>
          <td>{{ influencer.platform }}</td>
          <td>{{ influencer.status }}</td>
          <td>
            <button 
              v-if="influencer.flagged === 0" 
              @click="flagInfluencer(influencer)" 
              class="btn flag-button">
              <i class="fa-solid fa-xmark"></i> Flag
            </button>
            <button 
              v-if="influencer.flagged === 1" 
              @click="unflagInfluencer(influencer)" 
              class="btn unflag-button">
              <i class="fa-solid fa-flag"></i> Unflag
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InfluencerRequest',
  data() {
    return {
      influencers: []
    };
  },
  methods: {
    fetchInfluencerRequests() {
      axios.get('http://127.0.0.1:5000/influencer_resources', {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.influencers = response.data.data;
      })
      .catch(error => {
        console.error('Error fetching influencer requests:', error);
      });
    },

    flagInfluencer(influencer) {
      axios.delete(`http://127.0.0.1:5000/admin/influencer/${influencer.influencer_id}/flagging`, {}, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        influencer.flagged = 1;
        this.fetchInfluencerRequests();
        alert(`${influencer.name} flagged successfully!`);
      })
      .catch(error => {
        console.error('Error flagging influencer:', error);
        alert('Failed to flag the influencer.');
      });
    },

    unflagInfluencer(influencer) {
      axios.delete(`http://127.0.0.1:5000/admin/influencer/${influencer.influencer_id}/unflagging`, {}, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        influencer.flagged = 0;
        this.fetchInfluencerRequests();
        alert(`${influencer.name} unflagged successfully!`);
      })
      .catch(error => {
        console.error('Error unflagging influencer:', error);
        alert('Failed to unflag the influencer.');
      });
    }
  },

  created() {
    this.fetchInfluencerRequests();
  }
};
</script>

<style scoped>
/* Table styling */
.influencer-table {
  width: 100%;
  background-color: #343a40;
  color: #ffffff;
  border-collapse: collapse;
  margin-top: 20px;
}

.influencer-table th,
.influencer-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #495057;
}

.influencer-table th {
  background-color: #212529;
  color: #adb5bd;
}

.influencer-row:hover {
  background-color: #495057;
}

/* Button styles */
.btn {
  padding: 8px 12px;
  border-radius: 0px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.3s, transform 0.3s;
}

.flag-button {
  background-color: #dc3545; /* Red for flagging */
  color: white;
}

.flag-button:hover {
  background-color: #c82333;
  transform: scale(1.05);
}

.unflag-button {
  background-color: #ffc107; /* Yellow for unflagging */
  color: black;
}

.unflag-button:hover {
  background-color: #e0a800;
  transform: scale(1.05);
}
</style>
