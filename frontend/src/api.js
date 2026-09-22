const API_BASE_URL = "http://127.0.0.1:8000";


export async function login(email) {
    const response = await fetch(
        `${API_BASE_URL}/auth/login`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email: email,
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Login failed."
        );
    }

    return data;
}


export async function sendMessage(message) {
    const response = await fetch(
        `${API_BASE_URL}/chat?message=${encodeURIComponent(message)}`,
        {
            method: "POST",
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Request failed."
        );
    }

    return data;
}


export async function getUsers() {
    const response = await fetch(
        `${API_BASE_URL}/users`
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Could not fetch users."
        );
    }

    return data;
}