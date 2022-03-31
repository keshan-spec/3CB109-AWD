// login form
import React, { useState } from 'react';

export const Login = () => {
    const [mail, setMail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        fetch('http://ysjcs.net:5010/api/v1/login', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                // "Access-Control-Allow-Credentials": "true",
                // "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
                // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            },
            body: JSON.stringify({
                'email': mail,
                password
            })
        }).then(res => {
            res.json().then(data => console.log(data));

            if (res.status === 200) {
                // window.location.href = '/';
                setError('Sucess login');
            } else {
                setError('Invalid credentials');
            }
        }).catch(err => {
            console.log(err);
        })
    };

    return (
        <div className="login">
            <h1>Login</h1>
            <span>{error}</span>
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
                <button type="submit">Login</button>
            </form>
        </div>
    )
}