// register 
import React, { useState } from 'react';

export const Register = () => {
    const [mail, setMail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

    };

    return (
        <div className="login">
            <h1>Register</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    value={mail}
                    onChange={(event) => setMail(event.target.value)}
                    placeholder="Your email"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    placeholder="Your secret password"
                />
            </form>
        </div>
    )
}