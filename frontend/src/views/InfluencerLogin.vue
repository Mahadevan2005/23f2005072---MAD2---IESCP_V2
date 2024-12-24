<template>
  <div class="heading">
    <h1 class="iescp-title">Influencer Engagement & Sponsorship Coordination Platform</h1>
  </div>
  <MainNavbar />
  <div class="influencer-login">
    <div class="container d-flex justify-content-center align-items-center vh-100">
      <div class="login-card shadow-lg p-5 rounded">
        <h5 class="card-title text-center mb-4 text-secondary">Influencer Login</h5>
        <form @submit.prevent="influencerLogin">
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
          <br>
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
          <br />
          <button type="submit" class="submit-button">Login</button>
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          <br /><br />
          <div style="text-align: center">
            <a href="/" style="font-size: larger">Go to Home</a>
          </div>
          <br>
          <div style="text-align: center">
            <a href="/influencer_register" style="font-size: larger">Register as an Influencer</a>
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
  name: 'InfluencerLogin',
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
    influencerLogin() {
      axios
        .post('http://127.0.0.1:5000/influencer/login', {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          if (response.status === 200) {
            // Store username and redirect
            localStorage.setItem('influencer_id', response.data.influencer_id);
            localStorage.setItem('username', this.username);
            localStorage.setItem('email', this.email);
            localStorage.setItem('authToken', response.data.token);
            localStorage.setItem('category', response.data.category);
            localStorage.setItem('niche', response.data.niche);
            localStorage.setItem('reach', response.data.reach);
            localStorage.setItem('platform', response.data.platform);

            this.$router.push('/influencer_dashboard');
          } else {
            this.errorMessage = 'Invalid Influencer credentials';
          }
        })
        .catch((error) => {
          console.error('Error during login:', error);
          if (error.response) {
            if (error.response.status === 401) {
              this.errorMessage = 'Incorrect password or email';
            } else if (error.response.status === 403) {
              if (error.response.data.message === 'Your account is flagged.') {
                this.errorMessage = 'Your account has been flagged. Contact support for assistance.';
              } else {
                this.errorMessage = 'Account does not exist.';
              }
            } else if (error.response.status === 404) {
              this.errorMessage = 'Influencer account does not exist';
            } else {
              this.errorMessage = 'An error occurred. Please try again.';
            }
          } else {
            this.errorMessage = 'An error occurred. Please try again.';
          }
        });
    },
  },
};
</script>

<style>
.influencer-login {
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

.iescp-title {
  font-size: 2rem;
  font-family: 'Georgia', serif; /* Beautiful and elegant font */
  color: #283618;
  text-shadow: 2px 2px #e3d5ca; /* Soft shadow for an appealing effect */
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

.alert {
  border-radius: 10px;
  margin-top: 10px;
}

.form-label {
  font-size: 1rem;
  color: #555; /* Soft gray */
  margin-bottom: 8px;
  display: block;
  font-weight: bold;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 15px;
  font-size: 1.2rem;
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


.form-control-lg {
  height: calc(2.25rem + 2px); /* Increase the height of input fields */
  font-size: 1.1rem; /* Slightly larger font size for input fields */
}

.btn-custom {
  background-color: #002bea; /* Green color for the button */
  color: white; /* White text for contrast */
  border: none;
}

.btn-custom:hover {
  background-color: #218838; /* Darker green on hover */
}

.btn-lg {
  font-size: 1.1rem; /* Larger font size for the button */
  padding: 0.5rem 1rem; /* Increase padding for better button size */
}
</style>
