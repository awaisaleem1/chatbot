import { useState } from "react";

import Login from "./Login";
import Chat from "./Chat";


function App() {

    const [userEmail, setUserEmail] =
        useState(
            localStorage.getItem("userEmail")
        );


    const handleLogin = (email) => {

        localStorage.setItem(
            "userEmail",
            email
        );

        setUserEmail(email);
    };


    const handleLogout = () => {

        localStorage.removeItem(
            "userEmail"
        );

        setUserEmail(null);
    };


    if (!userEmail) {

        return (
            <Login
                onLogin={handleLogin}
            />
        );

    }


    return (
        <Chat
            email={userEmail}
            onLogout={handleLogout}
        />
    );
}


export default App;