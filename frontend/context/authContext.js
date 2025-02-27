import { createContext, useState, useEffect } from "react"
import { login, registerUser, logout, refreshAccessToken } from "../services/authService.js"

export const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null)

    useEffect(() => {
        const token = localStorage.getItem("accessToken")
        if(token)
            setUser({token})
    }, [])

    const loginUser = async (username, password) => {
        const data = await login(username, password)
        if(data.access)
            setUser({ token: data.access })
    }

    const logoutUser = () => {
        logout()
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, loginUser, logoutUser }}>
            {children}
        </AuthContext.Provider>
    )
}