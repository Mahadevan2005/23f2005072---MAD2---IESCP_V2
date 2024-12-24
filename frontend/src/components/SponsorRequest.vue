<template>
  <div>
    <h2>Sponsor Requests</h2>
    <table class="sponsor-table">
      <thead>
        <tr>
          <th>Sponsor Name</th>
          <th>E-mail</th>
          <th>Company Name</th>
          <th>Industry</th>
          <th>Budget</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sponsor in sponsors" :key="sponsor.sponsor_id" class="sponsor-row">
          <td>{{ sponsor.sponsor_name }}</td>
          <td>{{ sponsor.email }}</td>
          <td>{{ sponsor.company_name }}</td>
          <td>{{ sponsor.industry }}</td>
          <td>{{ sponsor.budget }}</td>
          <td>{{ sponsor.status }}</td>
          <td>
            <button 
              v-if="sponsor.status !== 'approved'" 
              @click="approveSponsor(sponsor)" 
              class="btn approve-button">
              <i class="fa-solid fa-check"></i> Approve
            </button>
            <button 
              v-if="sponsor.flagged === 0" 
              @click="flagSponsor(sponsor)" 
              class="btn flag-button">
              <i class="fa-solid fa-xmark"></i> Flag
            </button>
            <button 
              v-if="sponsor.flagged === 1" 
              @click="unflagSponsor(sponsor)" 
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
  name: 'SponsorRequest',
  data() {
    return {
      sponsors: []
    };
  },
  methods: {
    fetchSponsorRequests() {
      axios.get('http://127.0.0.1:5000/sponsor_resources', {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.sponsors = response.data.data;
      })
      .catch(error => {
        console.error('Error fetching sponsor requests:', error);
      });
    },

    approveSponsor(sponsor) {
      axios.put(`http://127.0.0.1:5000/admin/sponsor/${sponsor.sponsor_id}/approve`, {}, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        sponsor.approved = 1;
        this.fetchSponsorRequests();
        alert(`${sponsor.sponsor_name} approved successfully!`);
      })
      .catch(error => {
        console.error('Error approving sponsor:', error);
        alert('Failed to approve the sponsor.');
      });
    },

    flagSponsor(sponsor) {
      axios.delete(`http://127.0.0.1:5000/admin/sponsor/${sponsor.sponsor_id}/flagging`, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        sponsor.flagged = 1;
        this.fetchSponsorRequests();
        alert(`${sponsor.sponsor_name} flagged successfully!`);
      })
      .catch(error => {
        console.error('Error flagging sponsor:', error);
        alert('Failed to flag the sponsor.');
      });
    },

    unflagSponsor(sponsor) {
      axios.delete(`http://127.0.0.1:5000/admin/sponsor/${sponsor.sponsor_id}/unflagging`, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        sponsor.flagged = 0;
        this.fetchSponsorRequests();
        alert(`${sponsor.sponsor_name} unflagged successfully!`);
      })
      .catch(error => {
        console.error('Error unflagging sponsor:', error);
        alert('Failed to unflag the sponsor.');
      });
    }
  },

  created() {
    this.fetchSponsorRequests();
  }
};
</script>

<style scoped>
/* Table styling */
.sponsor-table {
  width: 100%;
  background-color: #343a40;
  color: #ffffff;
  border-collapse: collapse;
  margin-top: 20px;
}

.sponsor-table th,
.sponsor-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #495057;
}

.sponsor-table th {
  background-color: #212529;
  color: #adb5bd;
}

.sponsor-row:hover {
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

.approve-button {
  background-color: #09f071; /* Green for approval */
  color: white;
}

.approve-button:hover {
  background-color: #218838;
  transform: scale(1.05);
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
