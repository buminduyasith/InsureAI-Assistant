"use client"
import { useState } from "react";
import { login, getUserClaims } from "@/app/services/authService";
import { useRouter } from "next/navigation";

export default function LoginForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const router = useRouter();
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            setError(""); 
            await login(email, password);
            const resposne = await getUserClaims()
            if(resposne.claims.role == "Admin"){
                router.push("/dashboard");
            }
            else{
                router.push("/chat");
            }
        } catch (err:any) {
            setError(err.message || "An error occurred");
        }
    };

    return (
        <div className="d-flex justify-content-center align-items-center vh-100">
            <div className="card p-4 shadow-lg" style={{ width: "350px" }}>
                <h3 className="text-center mb-4">AI Insurance Assistant</h3>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">
                            Email
                        </label>
                        <input
                            type="email"
                            className="form-control"
                            id="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password" className="form-label">
                            Password
                        </label>
                        <input
                            type="password"
                            className="form-control"
                            id="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    {error && <div className="alert alert-danger">{error}</div>}
                    <button type="submit" className="btn btn-primary w-100">
                        Log In
                    </button>
                </form>
                <p className="mt-3 text-center">
                    Don&apos;t have an account? <a href="/signup">Sign up</a>
                </p>
            </div>
        </div>
    );
}
