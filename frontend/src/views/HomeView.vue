<template>
  <div class="home">
    <!-- App Heading -->
    <div class="app-heading">
      <h1>Influencer Engagement and Sponsorship Co-ordination Platform</h1>
    </div>

    <MainNavbar />

    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-text">
        <h1 class="iescp-title">Engage with Influencers Effortlessly</h1>
        <p class="hero-description">Your ultimate solution for coordinating sponsorships and managing influencer engagements.</p>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section">
      <h2 class="section-title">Why Choose Us?</h2>
      <div class="features-grid">
        <div class="feature-item">
          <h3 class="feature-title">Streamlined Sponsorships</h3>
          <p class="feature-description">Manage and coordinate sponsorships easily with real-time analytics.</p>
        </div>
        <div class="feature-item">
          <h3 class="feature-title">Comprehensive Engagement</h3>
          <p class="feature-description">Track influencer reach, engagement, and performance across multiple platforms.</p>
        </div>
        <div class="feature-item">
          <h3 class="feature-title">Seamless Communication</h3>
          <p class="feature-description">Communicate with influencers directly and streamline the campaign process.</p>
        </div>
      </div>
    </div>

    <!-- Call to Action Section -->
    <div class="cta-section">
      <h2 class="cta-title">Join the Revolution in Influencer Marketing</h2>
      <p class="cta-description">Create your account today and start connecting with the best influencers around the world.</p>
    </div>
  </div>
</template>

<script>
import MainNavbar from '@/components/MainNavbar.vue';

export default {
  name: 'HomeView',
  components: {
    MainNavbar,
  },
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f7f7f7; /* Soft background */
  color: #333;
}

/* App Heading */
.app-heading {
  text-align: center;
  margin-top: 20px;
  font-size: 1.75rem;
  font-weight: bold;
  color: #333; /* Dark gray for contrast */
}

/* Hero Section */
.hero-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 10px; /* More padding for a spacious look */
  background-color: #fff; /* White background for a clean look */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

.iescp-title {
  font-size: 2.5rem; /* Slightly larger font for emphasis */
  font-family: 'San Francisco', sans-serif; /* Clean font style */
  color: #1d1d1f; /* Darker color for better readability */
  margin-bottom: 10px;
}

.hero-description {
  font-size: 1.2rem;
  color: #555; /* Soft gray for description */
}

/* Features Section */
.features-section {
  padding: 20px;
  background-color: #ffffff; /* White background */
}

.section-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 40px;
  color: #333; /* Dark gray */
}

.features-grid {
  display: flex;
  justify-content: space-between;
  gap: 30px;
}

.feature-item {
  background-color: #f9f9f9; /* Light gray for contrast */
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  flex: 1;
}

.feature-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333; /* Dark gray */
}

.feature-description {
  font-size: 1rem;
  color: #666; /* Soft gray */
}

/* Call to Action Section */
.cta-section {
  text-align: center;
  padding: 60px;
  background-color: #007aff; /* Apple-like blue */
  color: white;
}

.cta-title {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.cta-description {
  font-size: 1.2rem;
}
</style>
