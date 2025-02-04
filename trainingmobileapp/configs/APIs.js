import axios from "axios";

// const BASE_URL = 'https://dinhkhoi1205.pythonanywhere.com/';
const BASE_URL = 'http://192.168.50.32:8000/'

export const endpoints = {
    'categories' : '/categories/',
    'activities' : '/activities/',
    'participations' : (activityId) => `/activities/${activityId}/participations/`,
    'activity-details': (activityId) => `/activities/${activityId}/`,
    'comments': (activityId) => `/activities/${activityId}/comments/`,
}

export default axios.create({
    baseURL: BASE_URL
})