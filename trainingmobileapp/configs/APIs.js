import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";

// const BASE_URL = 'https://dinhkhoi1205.pythonanywhere.com/';
const BASE_URL = 'http://192.168.50.32:8000/'

export const endpoints = {
    'categories' : '/categories/',
    'activities' : '/activities/',
    'participation' : '/participations/',
    'participation_activity' : (activityId) => `/activities/${activityId}/participations/`,
    'activity_details': (activityId) => `/activity-details/${activityId}/`,
    'comments': (activityId) => `/activity-details/${activityId}/comments/`,
    'login': '/o/token/',
    'current_user': '/users/current-user/',
    'register': '/users/',
    'activity_register': (activityId) => `/activity-details/${activityId}/register/`,
    'post_comment' : (activityId) => `/activity-details/${activityId}/comments/`
}

export const authApis = async () => {
    const token = await AsyncStorage.getItem("token");
    return axios.create({
        baseURL: BASE_URL,
        headers: {
            'Authorization' : `Bearer ${token}`
        }
    })
}

export default axios.create({
    baseURL: BASE_URL
})