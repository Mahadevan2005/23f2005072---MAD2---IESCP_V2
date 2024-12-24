<template>
  <div class="heading">
    <h1 class="iescp-title">Influencer Engagement & Sponsorship Coordination Platform</h1>
  </div>
  <MainNavbar />
  <div class="sponsor-login">
    <div class="container d-flex justify-content-center align-items-center vh-100">
      <div class="login-card shadow-lg p-5 rounded">
        <h5 class="card-title text-center mb-4 text-secondary">Sponsor Login</h5>
        <form @submit.prevent="sponsorLogin">
          <div class="form-group">
            <label for="email" class="form-label">E-mail</label>
            <div class="input-group">
              <div class="input-group-prepend">
                <span class="input-group-text"><i class="fas fa-user"></i></span>
              </div>
              <input
                type="email"
                v-model="email"
                class="form-control form-control-lg"
                id="email"
                required
                placeholder="Enter your email id"
              />
            </div>
          </div>
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <div class="input-group">
              <div class="input-group-prepend">
                <span class="input-group-text"><i class="fas fa-lock"></i></span>
              </div>
              <input
                type="password"
                v-model="password"
                class="form-control form-control-lg"
                id="password"
                required
                placeholder="Enter your password"
              />
            </div>
          </div>
          <!-- <br> -->
          <button type="submit" class="submit-button">Login</button>
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          <br><br>
          <div style="text-align: center">
            <a href="/" style="font-size: larger">Go to Home</a>
          </div>
          <br>
          <div style="text-align: center">
            <a href="/sponsor_register" style="font-size: larger">Register as an Sponsor</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MainNavbar from '@/components/MainNavbar.vue';

export default {
  name: 'SponsorLogin',
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
    sponsorLogin() {
      axios.post('http://127.0.0.1:5000/sponsor/login', {
          email: this.email,
          password: this.password,
        })
        .then(response => {
          if (response.status === 200 && response.data.role === 'sponsor') {
            localStorage.setItem('sponsor_id', response.data.sponsor_id);
            localStorage.setItem('authToken', response.data.token);
            this.$router.push('/sponsor_dashboard'); 
          } else {
            this.errorMessage = 'Invalid Sponsor credentials';
          }
        })
        .catch(error => {
          if (error.response) {
            switch (error.response.status) {
              case 401:
                this.errorMessage = 'Incorrect password or email';
                break;
              case 403:
                this.errorMessage = error.response.data.message === 'Your account is pending approval from the admin.'
                  ? 'Your account is pending admin approval. Please try again later.'
                  : 'Your account has been flagged. Contact support for assistance.';
                break;
              case 404:
                this.errorMessage = 'Account does not exist';
                break;
              default:
                this.errorMessage = 'An error occurred. Please try again.';
            }
          } else {
            this.errorMessage = 'An error occurred. Please try again.';
          }
        });
    },
  }
};
</script>

<style scoped>
.sponsor-login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 75vh;
  background-color: #f7f7f7; /* Light background */
}

.login-card {
  background-color: #ffffff;
  width: 400px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  padding: 20px;
}

.heading {
  text-align: center;
  margin-top: 20px;
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

.iescp-title {
  font-size: 2rem;
  color: #283618;
  font-family: 'Georgia', serif;
  text-shadow: 2px 2px #e3d5ca;
}

.card-title {
  color: #333; /* Dark gray for contrast */
  font-family: 'San Francisco', sans-serif; /* Clean font */
  font-size: 1.8rem;
  margin-bottom: 20px;
  text-align: center;
}

input[type="text"],
input[type="password"] {
  width: 75%;
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc; /* Light border */
  border-radius: 6px;
  transition: border-color 0.3s ease;
}

input[type="email"],
input[type="email"] {
  width: 75%;
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc; /* Light border */
  border-radius: 6px;
  transition: border-color 0.3s ease;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}


.form-label {
  font-size: 1rem;
  color: #555; /* Soft gray */
  margin-bottom: 8px;
  display: block;
  font-weight: bold;
}

.input-group-text {
  background-color: #e9ecef;
}

.form-control-lg {
  font-size: 1.1rem;
}

.btn-custom {
  background-color: #007aff;
  color: white;
  font-size: 1.1rem;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
}

.btn-custom:hover {
  background-color: #0056b3;
}

.alert {
  border-radius: 8px;
  margin-top: 10px;
  font-size: 0.9rem;
}


.error-message {
  color: red;
  text-align: center;
  margin-top: 15px;
  font-size: 1.2rem;
}

.nav-link {
  font-size: larger;
  /* color: #007bff; */
  text-align: center;
  text-decoration: none;
}
</style>
