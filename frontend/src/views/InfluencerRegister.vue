<template>
  <MainNavbar />
  <div class="register-influencer">
    <h2>Influencer Registration</h2>
    <div class="form-card">
      <form @submit.prevent="influencerRegister">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required>
        </div>
        <div class="form-group">
          <label for="email">E-mail</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <div class="form-group">
          <label for="category">Category</label>
          <input type="text" id="category" v-model="category" required>
        </div>
        <div class="form-group">
          <label for="niche">Niche</label>
          <input type="text" id="niche" v-model="niche" required>
        </div>
        <div class="form-group">
          <label for="reach">Reach</label>
          <input type="number" id="reach" v-model="reach" required>
        </div>
        <div class="form-group">
          <label for="platform">Platform</label>
          <input type="text" id="platform" v-model="platform" required>
        </div>
        <button type="submit" class="submit-button">Register</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MainNavbar from '@/components/MainNavbar.vue';

export default {
  name: 'InfluencerRegister',
  components: {
    MainNavbar,
  },
  data() {
    return {
      username: '',
      password: '',
      email: '',
      category: '',
      niche: '',
      reach: 0,
      platform: '',
      errorMessage: '',
    };
  },
  methods: {
    influencerRegister() {
      if (this.reach <= 0) {
        this.errorMessage = 'Reach must be greater than zero.';
        return;
      }

      axios
        .post('http://127.0.0.1:5000/influencer/register', {
          username: this.username,
          password: this.password,
          email: this.email,
          influencer_details: {
            name: this.username,
            password: this.password,
            email: this.email,
            category: this.category,
            niche: this.niche,
            reach: this.reach,
            platform: this.platform,
          },
        })
        .then((response) => {
          if (response.status === 201) {
            localStorage.setItem('authToken', response.data.token);
            this.$router.push('/influencer_login');
          }
        })
        .catch((error) => {
          console.log(error);
          this.errorMessage = 'Registration failed. Please try again.';
        });
    },
  },
};
</script>

<style scoped>
.register-influencer {
  max-width: 600px; /* Reduced the width for a smaller card */
  margin: auto;
  padding: 20px; /* Reduced padding for a smaller card */
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  font-family: 'Arial', sans-serif;
  margin-bottom: 15px; /* Reduced bottom margin */
  font-size: 1.4rem; /* Slightly smaller font size */
}

.form-group {
  margin-bottom: 15px; /* Reduced margin between form elements */
}

label {
  display: block;
  margin-bottom: 3px; /* Less space between label and input */
  font-weight: bold;
  color: #555;
  font-size: 0.9rem; /* Smaller label font size */
}

input[type="text"],
input[type="password"],
input[type="number"] {
  width: 100%;
  padding: 8px; /* Reduced padding for a more compact feel */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem; /* Slightly smaller font size */
  transition: border-color 0.3s;
}


input[type="email"],
input[type="email"],
input[type="email"] {
  width: 100%;
  padding: 8px; /* Reduced padding for a more compact feel */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem; /* Slightly smaller font size */
  transition: border-color 0.3s;
}

input[type="text"]:focus,
input[type="password"]:focus,
input[type="number"]:focus {
  border-color: #007BFF;
  outline: none;
}

.submit-button {
  width: 100%;
  padding: 8px; /* Reduced padding for a smaller button */
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem; /* Slightly smaller font size */
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px; /* Reduced space before error message */
  font-size: 0.85rem; /* Smaller error message font */
}
</style>
