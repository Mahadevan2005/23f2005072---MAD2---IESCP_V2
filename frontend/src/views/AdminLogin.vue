<template>
   <div class="heading">
    <h1 class="iescp-title">Influencer Engagement & Sponsorship Coordination Platform</h1>
  </div>
  <MainNavbar />
  <div class="admin-login">
    <div class="login-container">
      <h2>Admin Login</h2>
      <div class="form-card">
        <form @submit.prevent="adminLogin">
          <div class="form-group">
            <label for="email">E-mail</label>
            <input type="email" id="email" v-model="email" required placeholder="Enter your email id" />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required placeholder="Enter your password" />
          </div>
          <button type="submit" class="submit-button">Login</button>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <h1> </h1>
          <a href="/" style="font-size: larger">Go to Home</a>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MainNavbar from '@/components/MainNavbar.vue';

export default {
  name: 'AdminLogin',
  components: {
    MainNavbar,
  },
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    adminLogin() {
      axios
        .post('http://127.0.0.1:5000/admin/login', {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          if (response.data.role === 'admin') {
            localStorage.setItem('authToken', response.data.token);
            this.$router.push('/admin_dashboard');
          } else {
            this.errorMessage = 'Invalid admin credentials';
          }
        })
        .catch(() => {
          this.errorMessage = 'Incorrect email or password.';
        });
    },
  },
};
</script>

<style scoped>
.admin-login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 75vh;
  background-color: #f7f7f7; /* Light background */
}

.heading {
  text-align: center;
}

.login-container {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15); /* Subtle shadow for depth */
  text-align: center;
}

h2 {
  color: #333; /* Dark gray for contrast */
  font-family: 'San Francisco', sans-serif; /* Clean font */
  font-size: 1.8rem;
  margin-bottom: 20px;
}

.form-card {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  font-size: 1rem;
  color: #555; /* Soft gray */
  margin-bottom: 8px;
  display: block;
  font-weight: bold;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc; /* Light border */
  border-radius: 6px;
  transition: border-color 0.3s ease;
}



input[type="email"],
input[type="email"] {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc; /* Light border */
  border-radius: 6px;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #007aff; /* Apple-like blue */
  outline: none;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #007aff; /* Apple-like blue */
  color: white;
  font-size: 1.1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0056b3; /* Darker blue on hover */
}

.error-message {
  color: red;
  margin-top: 15px;
  font-size: 1.2rem;
}
</style>
