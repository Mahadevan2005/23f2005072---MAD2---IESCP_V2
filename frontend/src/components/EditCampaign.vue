<template>
  <br>
  <button @click="goToAllCampaigns" class="back-button">Back</button>
  <div class="edit-campaign">
    <h2>Edit Campaign</h2>
    <div v-if="campaign.flagged === 1" class="flagged-message">
      This campaign is flagged and cannot be edited.
    </div>
    <form @submit.prevent="submitEdit" v-if="campaign.flagged !== 1">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="campaign.name" required :disabled="campaign.flagged === 1" />
      </div>

      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="campaign.description" required :disabled="campaign.flagged === 1"></textarea>
      </div>

      <div class="form-group">
        <label for="niche">Niche:</label>
        <input type="text" id="niche" v-model="campaign.niche" :disabled="campaign.flagged === 1" />
      </div>

      <div class="form-group">
        <label for="start_date">Start Date:</label>
        <input type="date" id="start_date" v-model="campaign.start_date" required :disabled="campaign.flagged === 1" />
      </div>

      <div class="form-group">
        <label for="end_date">End Date:</label>
        <input type="date" id="end_date" v-model="campaign.end_date" required :disabled="campaign.flagged === 1" />
      </div>

      <div class="form-group">
        <label for="budget">Budget:</label>
        <input type="number" id="budget" v-model="campaign.budget" required :disabled="campaign.flagged === 1" />
      </div>

      <div class="form-group">
        <label for="visibility">Visibility:</label>
        <select id="visibility" v-model="campaign.visibility" required :disabled="campaign.flagged === 1">
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
      </div>

      <div class="form-group">
        <label for="goals">Goals:</label>
        <textarea id="goals" v-model="campaign.goals" required :disabled="campaign.flagged === 1"></textarea>
      </div>

      <button type="submit" class="submit-button" :disabled="campaign.flagged === 1">Save Changes</button>
    </form>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      campaign: {
        name: '',
        description: '',
        niche: '',
        start_date: '',
        end_date: '',
        budget: '',
        visibility: '',
        goals: '',
        flagged: 0,
        sponsor_id: '',
      },
      errorMessage: '',
      successMessage: '',
      companyBudget: 0,
    };
  },
  mounted() {
    this.fetchCampaign();
  },
  methods: {
    async fetchCampaign() {
      const token = localStorage.getItem('authToken');
      const campaignId = this.$route.params.id;
      try {
        const response = await fetch(`http://127.0.0.1:5000/sponsor/campaign/${campaignId}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': token,
          },
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to fetch campaign');
        }

        this.campaign = data.data;
        this.campaign.sponsor_id = data.data.sponsor_id;

        // Fetch company budget after campaign data is available
        this.fetchCompanyBudget(); 
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    async fetchCompanyBudget() {
      const token = localStorage.getItem('authToken');
      const sponsorId = this.campaign.sponsor_id;
      try {
        const response = await fetch(`http://127.0.0.1:5000/sponsor/company_budget`, {
          method: 'GET',
          headers: {
            'Authentication-Token': token,
            'Sponsor-ID': sponsorId,
          },
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Failed to fetch company budget');
        }

        this.companyBudget = data.company_budget; // Use the correct key
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    async submitEdit() {
  const token = localStorage.getItem('authToken');
  const campaignId = this.$route.params.id;

  // Date and budget validation logic
  if (new Date(this.campaign.end_date) < new Date()) {
    this.errorMessage = 'End date must be in the future.';
    return;
  }

  if (new Date(this.campaign.end_date) <= new Date(this.campaign.start_date)) {
    this.errorMessage = 'End date cannot be earlier than start date or same as start date.';
    return;
  }

  if (this.campaign.budget <= 0) {
    this.errorMessage = 'Budget must be greater than 0.';
    return;
  }

  if (this.campaign.budget > this.companyBudget) {
    this.errorMessage = `Campaign budget cannot exceed company budget of ${this.companyBudget}.`;
    return;
  }

  // Log the payload to see what is being sent
  console.log('Payload being sent to the server:', this.campaign);

  // Proceed with the API call after validations pass
  try {
    const response = await fetch(`http://127.0.0.1:5000/sponsor/campaign/${campaignId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': token,
      },
      body: JSON.stringify(this.campaign),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'Failed to edit campaign');
    }

    this.successMessage = 'Campaign updated successfully!';
    this.errorMessage = '';
    setTimeout(() => {
      this.successMessage = '';
    }, 3000);
  } catch (error) {
    this.errorMessage = error.message;
  }
},
    goToAllCampaigns() {
      this.$router.push('/sponsor_dashboard?view=allCampaigns');
    },
  },
};
</script>

<style scoped>
.edit-campaign {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  font-family: 'Arial', sans-serif;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input[type='text'],
input[type='date'],
input[type='number'],
select,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

input[type='text']:focus,
input[type='date']:focus,
input[type='number']:focus,
select:focus,
textarea:focus {
  border-color: #007BFF;
  outline: none;
}

textarea {
  height: 100px;
  resize: none;
}

.submit-button {
  width: 100%;
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 15px;
}

.success-message {
  color: green;
  text-align: center;
  margin-top: 15px;
}

.back-button {
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: #0056b3;
}

.flagged-message {
  color: red;
  text-align: center;
  margin-bottom: 15px;
}
</style>
