import { useEffect, useState } from "react";
import {
    getUsers,
    sendMessage
} from "./api";


function Chat({ email, onLogout }) {

    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);

    const [users, setUsers] = useState([]);

    const [loading, setLoading] = useState(false);


    const loadUsers = async () => {

        try {

            const data = await getUsers();

            setUsers(data);

        } catch (error) {

            console.error(error);

        }
    };


    useEffect(() => {

        loadUsers();

    }, []);


    const handleSend = async (event) => {

        event.preventDefault();

        if (!message.trim() || loading) {
            return;
        }


        const userMessage = message;

        setMessage("");


        setMessages((previous) => [
            ...previous,

            {
                role: "user",
                content: userMessage,
            },
        ]);


        try {

            setLoading(true);

            const result =
                await sendMessage(userMessage);


            setMessages((previous) => [
                ...previous,

                {
                    role: "assistant",
                    content: result.message,
                },
            ]);


            await loadUsers();

        } catch (error) {

            setMessages((previous) => [
                ...previous,

                {
                    role: "assistant",
                    content:
                        `Error: ${error.message}`,
                },
            ]);

        } finally {

            setLoading(false);

        }
    };


    return (
        <div className="app-container">


            {/* HEADER */}

            <header className="header">

                <div>

                    <h1>
                        AI User Manager
                    </h1>

                    <span>
                        Logged in as {email}
                    </span>

                </div>


                <button
                    onClick={onLogout}
                    className="logout-button"
                >
                    Logout
                </button>

            </header>


            <div className="content">


                {/* CHAT */}

                <main className="chat-section">

                    <div className="messages">

                        {messages.length === 0 && (

                            <div className="welcome">

                                <h2>
                                    How can I help?
                                </h2>

                                <p>
                                    Manage users using
                                    natural language.
                                </p>

                                <div className="examples">

                                    <p>
                                        "Add John with
                                        email
                                        john@example.com"
                                    </p>

                                    <p>
                                        "Update Awais's
                                        city to Lahore"
                                    </p>

                                    <p>
                                        "Delete
                                        john@example.com"
                                    </p>

                                    <p>
                                        "Show all users"
                                    </p>

                                </div>

                            </div>

                        )}


                        {messages.map(
                            (msg, index) => (

                                <div
                                    key={index}
                                    className={
                                        `message ${msg.role}`
                                    }
                                >
                                    {msg.content}
                                </div>

                            )
                        )}


                        {loading && (

                            <div className="message assistant">
                                Processing...
                            </div>

                        )}

                    </div>


                    <form
                        className="chat-input"
                        onSubmit={handleSend}
                    >

                        <input
                            type="text"
                            placeholder="Ask me to add, update, delete, or find a user..."
                            value={message}
                            onChange={(event) =>
                                setMessage(
                                    event.target.value
                                )
                            }
                            disabled={loading}
                        />


                        <button
                            type="submit"
                            disabled={
                                loading ||
                                !message.trim()
                            }
                        >
                            Send
                        </button>

                    </form>

                </main>


                {/* USERS */}

                <aside className="users-section">

                    <div className="users-header">

                        <h2>
                            Users
                        </h2>

                        <button
                            onClick={loadUsers}
                        >
                            Refresh
                        </button>

                    </div>


                    {users.length === 0 ? (

                        <p>
                            No users found.
                        </p>

                    ) : (

                        <div className="user-list">

                            {users.map(
                                (user) => (

                                    <div
                                        className="user-card"
                                        key={user.id}
                                    >

                                        <strong>
                                            {user.name ||
                                                "Unnamed User"}
                                        </strong>

                                        <span>
                                            {user.email}
                                        </span>

                                        {user.phone && (
                                            <span>
                                                📱 {user.phone}
                                            </span>
                                        )}

                                        {user.city && (
                                            <span>
                                                📍 {user.city}
                                            </span>
                                        )}

                                    </div>

                                )
                            )}

                        </div>

                    )}

                </aside>

            </div>

        </div>
    );
}


export default Chat;