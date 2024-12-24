<template>
  <MainNavbar />
  <div class="register-sponsor">
    <h2>Sponsor Registration</h2>
    <div class="form-card">
      <form @submit.prevent="sponsorRegister">
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
          <label for="company_name">Company Name</label>
          <input type="text" id="company_name" v-model="company_name" required>
        </div>
        <div class="form-group">
          <label for="company_budget">Company Budget</label>
          <input type="number" id="company_budget" v-model="company_budget" required>
        </div>
        <div class="form-group">
          <label for="industry">Industry</label>
          <input type="text" id="industry" v-model="industry" required>
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
  name: 'SponsorRegister',
  components: {
    MainNavbar,
  },
  data() {
    return {
      username: '',
      password: '',
      email: '',
      company_name: '',
      company_budget: 0,
      industry: '',
      errorMessage: '',
    };
  },
  methods: {
    sponsorRegister() {
      if (this.company_budget <= 0) {
        this.errorMessage = 'Company budget must be greater than or equal to 0.';
        return;
      }

      axios
        .post('http://127.0.0.1:5000/sponsor/register', {
          username: this.username,
          password: this.password,
          email: this.email,
          sponsor_details: {
            username: this.username,
            password: this.password,
            email: this.email,
            company_name: this.company_name,
            company_budget: this.company_budget,
            industry: this.industry,
          },
        })
        .then((response) => {
          if (response.status === 201) {
            alert('Your request has been sent to admin. Once approved, you can login.');
            localStorage.setItem('authToken', response.data.token);
            this.$router.push('/sponsor_login');
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
.register-sponsor {
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
input[type="password"],
input[type="number"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}


input[type="email"],
input[type="email"],
input[type="email"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
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
