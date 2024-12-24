<template>
  <div class="new-campaign">
    <h2>Create New Campaign</h2>
    <form @submit.prevent="submitCampaign">
      <div class="form-group">
        <label for="name">Campaign Name:</label>
        <input type="text" id="name" v-model="name" required />
      </div>
      <div class="form-group">
        <label for="niche">Niche:</label>
        <input type="text" id="niche" v-model="niche" required />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="description" required></textarea>
      </div>
      <div class="form-group">
        <label for="start-date">Start Date:</label>
        <input type="date" id="start-date" v-model="startDate" required />
      </div>
      <div class="form-group">
        <label for="end-date">End Date:</label>
        <input type="date" id="end-date" v-model="endDate" required />
      </div>
      <div class="form-group">
        <label for="budget">Budget:</label>
        <input type="number" id="budget" v-model="budget" required />
      </div>
      <div class="form-group">
        <label for="visibility">Visibility:</label>
        <select id="visibility" v-model="visibility" required>
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
      </div>
      <div class="form-group">
        <label for="goals">Goals:</label>
        <textarea id="goals" v-model="goals" required></textarea>
      </div>
      <button type="submit" class="submit-button">Create Campaign</button>
    </form>
    <p v-if="message" class="error-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NewCampaign',
  data() {
    return {
      sponsor_id: localStorage.getItem('sponsor_id'),
      name: '',
      niche: '',
      description: '',
      startDate: '',
      endDate: '',
      budget: '',
      visibility: 'public',
      goals: '',
      companyBudget: 0, // New field for company budget
      message: '',
    };
  },
  mounted() {
    this.getCompanyBudget(); // Fetch company budget on component mount
  },
  methods: {
    async getCompanyBudget() {
      const authToken = localStorage.getItem('authToken');
      const sponsorId = localStorage.getItem('sponsor_id');
      try {
        const response = await axios.get('http://127.0.0.1:5000/sponsor/company_budget', {
          headers: {
            'Authentication-Token': authToken,
            'Sponsor-ID': sponsorId,
          },
        });
        this.companyBudget = response.data.company_budget;
      } catch (error) {
        this.message = 'Error fetching company budget';
      }
    },
    submitCampaign() {
      const currentDate = new Date().toISOString().split('T')[0]; // Get current date in 'YYYY-MM-DD'

      // Validate if the end date is in the future
      if (this.endDate <= currentDate) {
        this.message = 'The end date must be in the future.';
        return;
      }

      // Validate the campaign budget against company budget
      if (this.budget > this.companyBudget) {
        this.message = `The campaign budget exceeds the company budget (${this.companyBudget}).`;
        return;
      }

      // Validate the budget amount
      if (this.budget <= 0) {
        this.message = 'The budget must be greater than 0.';
        return;
      }

      // Validate the date range
      if (this.endDate <= this.startDate) {
        this.message = 'The end date cannot be earlier than the start date or same as start date.';
        return;
      }

      const campaignData = {
        name: this.name,
        sponsor_id: this.sponsor_id,
        description: this.description,
        start_date: this.startDate,
        end_date: this.endDate,
        budget: this.budget,
        visibility: this.visibility,
        goals: this.goals,
        niche: this.niche,
      };

      const authToken = localStorage.getItem('authToken');
      // const userRole = localStorage.getItem('role');
        axios.post('http://127.0.0.1:5000/sponsor/campaign', campaignData, {
            headers: {
              'Authentication-Token': authToken,
              'Content-Type': 'application/json',
            },
          })
          .then(() => {
            alert('Campaign added successfully');
            this.$router.push('/sponsor_dashboard');
          })
          .catch((error) => {
            this.message = error.response
              ? error.response.data.message
              : 'An error occurred. Please try again.';
          });
    },
  },
};
</script>


<style scoped>
.new-campaign {
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

input[type="text"],
input[type="date"],
input[type="number"],
select,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

input[type="text"]:focus,
input[type="date"]:focus,
input[type="number"]:focus,
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
</style>
