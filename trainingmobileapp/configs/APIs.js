import axios from "axios";

// const BASE_URL = 'https://dinhkhoi1205.pythonanywhere.com/';
const BASE_URL = 'http://192.168.50.32:8000/'

export const endpoints = {
    'categories' : '/categories/',
    'activities' : '/activities/',
    'participations' : (activityId) => `/activities/${activityId}/participations/`,
    'activityDetail': (activityId) => `/activities/${activityId}/`,
    'comments': (activityId) => `/activities/${activityId}/comments/`,
    'login': '/o/token/',
    'current-user': '/users/current-user/',
    'register': '/users/'
}

export default axios.create({
    baseURL: BASE_URL
})