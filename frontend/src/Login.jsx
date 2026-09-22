import { useState } from "react";
import { login } from "./api";


function Login({ onLogin }) {

    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    const handleSubmit = async (event) => {

        event.preventDefault();

        setError("");

        if (!email.trim()) {
            setError("Please enter your email.");
            return;
        }

        try {

            setLoading(true);

            const result = await login(email);

            if (result.success) {

                onLogin(email);

            }

        } catch (error) {

            setError(error.message);

        } finally {

            setLoading(false);

        }
    };


    return (
        <div className="login-container">

            <div className="login-card">

                <h1>AI User Manager</h1>

                <p className="login-subtitle">
                    Sign in to manage users with AI
                </p>


                <form onSubmit={handleSubmit}>

                    <label>
                        Email
                    </label>

                    <input
                        type="email"
                        placeholder="admin@example.com"
                        value={email}
                        onChange={(event) =>
                            setEmail(event.target.value)
                        }
                    />


                    {error && (
                        <p className="error">
                            {error}
                        </p>
                    )}


                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading
                            ? "Signing in..."
                            : "Sign In"
                        }
                    </button>

                </form>

            </div>

        </div>
    );
}


export default Login;