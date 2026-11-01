import './LoginPage.css';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import ACMLogo from '../assets/images/uhd_acm_logo.jpg';

export function LoginPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [accountCreated, setAccountCreated] = useState(false);
    const [error, setError] = useState('');

    function handleSubmit(event) {
        event.preventDefault();
        if (!accountCreated) {
            setError('No account found. Check the box to "create" one.');
            return;
        }
        setError('');
        navigate('/dashboard');
    }

    return (
    <>
            <title>Login</title>
            <link rel="icon" type="image/svg+xml" href="../public/ai.webp" />
        <div className="container">
            <div className="design">
                <div className="left-side">
                    <img className="acmlogo" src={ACMLogo} alt="UHD ACM logo" />
                </div>

                <div className="middle">
                    <div className="middle-top">
                        <p className="welcome">Welcome to Canvas</p>
                        <p>Yilmaz</p>
                        <p>This is a barebones login page</p>
                    </div>

                    <form className="input-container" onSubmit={handleSubmit}>
                        <div className="input-fields">
                            <input
                                type="text"
                                autoComplete="email"
                                className="input-box"
                                placeholder="Email"
                                value={email}
                                onChange={(event) => setEmail(event.target.value)}
                            />
                            <div className="show-pass">
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    autoComplete="current-password"
                                    className="input-box"
                                    placeholder="Password"
                                    value={password}
                                    onChange={(event) => setPassword(event.target.value)}
                                />
                                <button
                                    type="button"
                                    className="show-hide"
                                    onClick={() => setShowPassword(!showPassword)}
                                >
                                    {showPassword ? 'Hide' : 'Show'}
                                </button>
                            </div>
                        </div>

                        {error && <p role="alert">{error}</p>}

                        
                        <button type="submit" className="login" disabled={!email || !password}>
                            Login
                        </button>

                        <label>
                            <input
                                type="checkbox"
                                checked={accountCreated}
                                onChange={() => setAccountCreated(!accountCreated)}
                            />
                            Check the box to "create" an account (theoretical stuff)
                        </label>
                    </form>
                </div>

                <div className="right-side"></div>
            </div>
        </div>
    </>
    );
}