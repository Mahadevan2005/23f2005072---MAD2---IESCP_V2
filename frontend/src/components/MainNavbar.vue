<template>
  <div class="navbar-container">
    <nav class="navbar">
      <div class="nav-links">
        <router-link to="/admin_login">
          <button>Admin Login</button>
        </router-link>
        <router-link to="/sponsor_login">
          <button>Sponsor Login</button>
        </router-link>
        <router-link to="/influencer_login">
          <button>Influencer Login</button>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'MainNavbar',
};
</script>

<style scoped>
.navbar-container {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: transparent; /* Make it transparent to blend with homepage */
  box-shadow: none; /* Remove shadow for a flat look */
  margin: 20px auto; /* Centers the navbar with margin */
}

.navbar {
  display: flex;
  justify-content: center;
  align-items: center;
}

.nav-links {
  display: flex;
  gap: 1.5rem; /* Spacing between buttons */
}

button {
  padding: 0.7rem 1.5rem; /* Larger button padding */
  background-color: #0b0bba;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 20px;
  transition: background-color 0.3s ease; /* Smooth transition for hover */
}

button:hover {
  background-color: #99582a; /* Hover effect with smooth transition */
}
</style>
