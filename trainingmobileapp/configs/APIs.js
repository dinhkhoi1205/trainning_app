import axios from "axios";

const BASE_URL = 'https://dinhkhoi1205.pythonanywhere.com';

export const endpoints = {
    'categories' : '/categories/'
}

export default axios.create({
    baseURL: BASE_URL
})