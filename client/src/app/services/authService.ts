import axios from "axios";

const API_BASE_URL = "http://localhost:8081"; // Replace with your actual backend URL

export const login = async (email: string, password: string) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/auth/login`, {
            email,
            password,
        });
        localStorage.setItem("authToken", response.data.token);
    } catch (error) {
        throw error.response ? error.response.data : new Error("Network Error");
    }
};


export const getUserClaims = async () => {
    try {
        // Retrieve the token from localStorage
        var token = localStorage.getItem("authToken");

        // Make a GET request to the API with the Authorization header
        const response = await axios.get(`${API_BASE_URL}/token/introspect`, {
            headers: {
                Authorization: `Bearer ${token}` // Include the token in the Authorization header
            }
        });

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : new Error("Network Error");
    }
};