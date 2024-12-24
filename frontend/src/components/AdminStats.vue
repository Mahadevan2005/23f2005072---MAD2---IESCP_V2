<template>
  <h1>App Statistics</h1>
  <br>
  <br>
  
  <div>
    <div class="chart-container">
      <h4>Overall Statistics</h4>
      <canvas id="overallStatsChart"></canvas>
    </div>
    <br>
    <br>
    <br>

    <!-- Bar chart for Influencer distribution by niche -->
    <div class="chart-container">
      <h4>Influencer Distribution by Niche</h4>
      <canvas id="nicheDistributionChart"></canvas>
    </div>
    <br>
    <br>
    <br>

    <!-- Bar chart for Campaigns distribution by Budget -->
    <div class="chart-container">
      <h4>Distribution of Campaigns by Budget</h4>
      <canvas id="campaignBudgetChart"></canvas>
    </div>

    <br>
    <br>
    <br>

    <!-- Bar chart for Influencers distribution by Reach -->
    <div class="chart-container">
      <h4>Distribution of Influencers by Reach</h4>
      <canvas id="influencerReachChart"></canvas>
    </div>

    <br>
    <br>
    <h1></h1>
    <br>
    <!-- New box container for the pie charts -->
    <div class="pie-chart-box-container">
      <h4>Influencer, Campaign, and Sponsor Statistics</h4>
      <div class="flex-container">
        <div class="pie-chart-container">
          <h4>Flagged vs Non-Flagged Influencers</h4>
          <div class="pie-chart-box">
            <canvas id="flaggedInfluencersChart"></canvas>
          </div>
        </div>

        <div class="pie-chart-container">
          <h4>Flagged vs Non-Flagged Campaigns</h4>
          <div class="pie-chart-box">
            <canvas id="flaggedCampaignsChart"></canvas>
          </div>
        </div>
      </div>

      <div class="flex-container">
        <div class="pie-chart-container">
          <h4>Flagged vs Non-Flagged Sponsors</h4>
          <div class="pie-chart-box">
            <canvas id="flaggedSponsorsChart"></canvas>
          </div>
        </div>

        <div class="pie-chart-container">
          <h4>Public vs Private Campaigns</h4>
          <div class="pie-chart-box">
            <canvas id="publicPrivateCampaignsChart"></canvas>
          </div>
        </div>
      </div>
    </div>
    <br>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'AdminStats',
  data() {
    return {
      overallStats: {},
      authToken: localStorage.getItem('authToken'),
    };
  },
  methods: {
    fetchOverallStats() {
      axios
        .get('http://127.0.0.1:5000/admin_overall_stats', {
          headers: {
            'Authentication-Token': this.authToken,
          },
        })
        .then((response) => {
          this.overallStats = response.data.data;
          this.renderOverallStatsChart();
          this.renderNicheDistributionChart(); 
          this.renderFlaggedInfluencersChart();
          this.renderFlaggedSponsorsChart();
          this.renderFlaggedCampaignsChart();
          this.renderPublicPrivateCampaignsChart(); 
          this.renderCampaignBudgetChart(); // Call for budget distribution chart
          this.renderInfluencerReachChart(); // Call for reach distribution chart
        })
        .catch((error) =>
          console.error('Error fetching overall statistics:', error)
        );
    },

    renderOverallStatsChart() {
      const ctx = document.getElementById('overallStatsChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: [
            'Total Sponsors',
            'Total Influencers',
            'Total Campaigns',
            'Total Ads',
          ],
          datasets: [
            {
              label: 'Count',
              data: [
                this.overallStats.total_sponsors,
                this.overallStats.total_influencers,
                this.overallStats.total_campaigns,
                this.overallStats.total_ads,
              ],
              backgroundColor: [
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(255, 99, 132, 0.8)',
              ],
              borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 99, 132, 1)',
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              enabled: true,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
            },
            x: {
              barThickness: 0,
            },
          },
        },
      });
    },

    renderNicheDistributionChart() {
      const ctx = document.getElementById('nicheDistributionChart').getContext('2d');
      
      const labels = Object.keys(this.overallStats.niche_distribution); // Get the niche names from overallStats
      const data = Object.values(this.overallStats.niche_distribution); // Get the counts for each niche

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Influencer Count by Niche',
              data: data,
              backgroundColor: 'rgba(153, 102, 255, 0.8)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              enabled: true,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },

    renderFlaggedInfluencersChart() {
      const ctx = document.getElementById('flaggedInfluencersChart').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Flagged Influencers', 'Non-Flagged Influencers'],
          datasets: [
            {
              label: 'Influencers',
              data: [
                this.overallStats.flagged_influencers,
                this.overallStats.non_flagged_influencers,
              ],
              backgroundColor: ['rgba(255, 99, 132, 0.8)', 'rgba(75, 192, 192, 0.8)'],
              borderColor: ['rgba(255, 99, 132, 1)', 'rgba(75, 192, 192, 1)'],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            tooltip: {
              enabled: true,
            },
          },
        },
      });
    },

    renderFlaggedSponsorsChart() {
      const ctx = document.getElementById('flaggedSponsorsChart').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Flagged Sponsors', 'Non-Flagged Sponsors'],
          datasets: [
            {
              label: 'Sponsors',
              data: [
                this.overallStats.flagged_sponsors,
                this.overallStats.non_flagged_sponsors,
              ],
              backgroundColor: ['rgba(153, 102, 255, 0.8)', 'rgba(255, 206, 86, 0.8)'],
              borderColor: ['rgba(153, 102, 255, 1)', 'rgba(255, 206, 86, 1)'],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            tooltip: {
              enabled: true,
            },
          },
        },
      });
    },

    renderFlaggedCampaignsChart() {
      const ctx = document.getElementById('flaggedCampaignsChart').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Flagged Campaigns', 'Non-Flagged Campaigns'],
          datasets: [
            {
              label: 'Campaigns',
              data: [
                this.overallStats.flagged_campaigns,
                this.overallStats.non_flagged_campaigns,
              ],
              backgroundColor: ['rgba(75, 192, 192, 0.8)', 'rgba(255, 99, 132, 0.8)'],
              borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            tooltip: {
              enabled: true,
            },
          },
        },
      });
    },

    renderPublicPrivateCampaignsChart() {
      const ctx = document.getElementById('publicPrivateCampaignsChart').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Public Campaigns', 'Private Campaigns'],
          datasets: [
            {
              label: 'Campaigns',
              data: [
                this.overallStats.public_campaigns,
                this.overallStats.private_campaigns,
              ],
              backgroundColor: ['rgba(153, 102, 255, 0.8)', 'rgba(255, 206, 86, 0.8)'],
              borderColor: ['rgba(153, 102, 255, 1)', 'rgba(255, 206, 86, 1)'],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            tooltip: {
              enabled: true,
            },
          },
        },
      });
    },

    renderCampaignBudgetChart() {
      const ctx = document.getElementById('campaignBudgetChart').getContext('2d');

      const labels = Object.keys(this.overallStats.budget_distribution); // Get the budget categories from overallStats
      const data = Object.values(this.overallStats.budget_distribution); // Get the counts for each budget category

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Campaign Count by Budget',
              data: data,
              backgroundColor: 'rgba(255, 99, 132, 0.8)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              enabled: true,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },

    renderInfluencerReachChart() {
      const ctx = document.getElementById('influencerReachChart').getContext('2d');

      const labels = Object.keys(this.overallStats.reach_distribution); // Get the reach categories from overallStats
      const data = Object.values(this.overallStats.reach_distribution); // Get the counts for each reach category

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Influencer Count by Reach',
              data: data,
              backgroundColor: 'rgba(255, 206, 86, 0.8)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              enabled: true,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
  },
  mounted() {
    this.fetchOverallStats();
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 75%;
  height: 400px; /* Adjust the height as needed */
}

.pie-chart-box-container {
  width: 100%; /* Match the width of chart containers */
  margin: auto; /* Center the container */
  text-align: center; /* Center the title and chart */
  border: 1px solid #ccc; /* Add border for visibility */
  border-radius: 5px; /* Rounded corners */
  background-color: #f9f9f9;
}

.flex-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.pie-chart-container {
  flex: 2; /* Ensure each pie chart container takes equal space */
  margin: 10px;
  text-align: center; /* Center the title and chart */
  border: 1px solid #ccc; /* Add border for visibility */
  border-radius: 5px; /* Rounded corners */
  background-color: #f9f9f9; /* Light background for contrast */
}

.pie-chart-box {
  width: 100%; /* Ensure pie charts take full width */
  height: 220px; /* Adjust the height as needed */
}
</style>