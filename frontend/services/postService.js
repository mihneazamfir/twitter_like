import axios from "axios"

const API_URL = "http://localhost:8000/api"

const getAuthHeaders = () => {
    return { headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` } }
}

export const fetchPosts = async () => {
    return axios.get(`${API_URL}/posts/`, getAuthHeaders())
}

