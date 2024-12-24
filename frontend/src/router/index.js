import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EditCampaign from '@/components/EditCampaign.vue'
import AllCampaigns from '@/components/AllCampaigns.vue'
import AvailableInfluencers from '@/components/AvailableInfluencers.vue'
import NewAdrequest from '@/components/NewAdrequest.vue'
import SponsorEditAdrequest from '@/components/SponsorEditAdrequest.vue'
import SponsorAdRequest from '@/components/SponsorAdRequest.vue'
import InfluencerNewAdrequest from '@/components/InfluencerNewAdrequest.vue'
import InfluencerEditAdrequest from '@/components/InfluencerEditAdrequest.vue'
import InfluencerProfileUpdate from '@/components/InfluencerProfileUpdate.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/admin_login',
    name: 'admin_login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AdminLogin.vue')
  },
  {
    path: '/influencer_login',
    name: 'influencer_login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/InfluencerLogin.vue')
  },
  {
    path: '/influencer_register',
    name: 'influencer_register',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/InfluencerRegister.vue')
  },
  {
    path: '/sponsor_login',
    name: 'sponsor_login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/SponsorLogin.vue')
  },
  {
    path: '/sponsor_register',
    name: 'sponsor_register',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/SponsorRegister.vue')
  },
  {
    path: '/admin_dashboard',
    name: 'admin_dashboard',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AdminDashboard.vue')
  },
  {
    path: '/sponsor_dashboard',
    name: 'sponsor_dashboard',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/SponsorDashboard.vue')
  },
  {
    path: '/influencer_dashboard',
    name: 'InfluencerDashboard',
    component: () => import(/* webpackChunkName: "about" */ '../views/InfluencerDashboard.vue'),
    props: true, // Allow route params to be passed as props
  },
  {
    path: '/all_campaigns',
    name: 'AllCampaigns',
    component: AllCampaigns,
  },
  {
      path: '/edit-campaign/:id',
      name: 'EditCampaign',
      component: EditCampaign,
  },
  {
    path: '/available_influencers/:campaignId/:campaignName', // Added campaignName parameter
    name: 'AvailableInfluencers',
    component: AvailableInfluencers,
  },
  {
    path: '/new_ad_request/:influencer_id/:campaign_id/:influencer_name/:campaign_name',
    name: 'NewAdrequest',
    component: NewAdrequest,
  },
  {
    path: '/ad_request/:id', // Make sure to match the parameter name
    name: 'SponsorEditAdRequest',
    component: SponsorEditAdrequest,
  },
  {
    path: '/all_adrequests', // Make sure to match the parameter name
    name: 'SponsorAdRequest',
    component: SponsorAdRequest,
  },
  {
    path: '/influencer/ad_request/:campaign_id/:campaign_name',
    name: 'InfluencerNewAdrequest',  // Route name for the ad request form
    component: InfluencerNewAdrequest,
  },
  {
    path: '/influencer_specific_ad_request/:id', // Make sure to match the parameter name
    name: 'InfluencerEditAdRequest',
    component: InfluencerEditAdrequest,
  },
  {
    path: '/influencer_profile_update',
    name: 'InfluencerProfileUpdate',
    component: InfluencerProfileUpdate
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
