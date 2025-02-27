import axios from "axios"

const API_URL = "http://localhost:8000/api"

export const login = async (username, password) => {
    const response = await axios.post(`${API_URL}/auth/login/`, {username, password})
    if (response.data.access) {
        localStorage.setItem("accessToken", response.data.access)
        localStorage.setItem("refreshToken", response.data.refresh)
    }
    return response.data
}

export const registerUser = async (username, password, email, first_name, last_name) => {
    return axios.post(`${API_URL}/auth/register/`, {username, password, email, first_name, last_name})
}

export const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem("refreshToken")
    if (!refreshToken)
        return null
    const response = await axios.post(`${API_URL}/auth/refresh/`, {refresh: refreshToken})
    if (response.data.access) {
        localStorage.setItem("accessToken", response.data.access)
    }
    return response.data.access
}

export const logout = async () => {
    await axios.post(`${API_URL}/auth/logout/`, {refresh: localStorage.getItem("refreshToken")})
    localStorage.removeItem("accessToken")
    localStorage.removeItem("refreshToken")
}