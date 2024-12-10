import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_AUTH_URL
export const login = async (email: string, password: string) : Promise<any> => {
    try {
        const response = await axios.post(`${API_BASE_URL}/auth/login`, {
            email,
            password,
        });
        localStorage.setItem("authToken", response.data.token);
    } catch (error:any) {
        throw error.response ? error.response.data : new Error("Network Error");
    }
};


export const getUserClaims = async () => {
    try {
        var token = localStorage.getItem("authToken");
        const response = await axios.get(`${API_BASE_URL}/token/introspect`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error: any) {
        throw error.response ? error.response.data : new Error("Network Error");
    }
};