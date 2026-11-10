import './LoginPage.css';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import ACMLogo from '../assets/images/uhd_acm_logo.jpg';
import { login, register } from '../api.js';

export function LoginPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [createMode, setCreateMode] = useState(false);
    const [name, setName] = useState('');
    const [isProfessor, setIsProfessor] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        setError('');

        if (createMode && password.length < 8) {
            setError('Password must be at least 8 characters.');
            return;
        }

        setLoading(true);
        try {
            if (createMode) {
                await register({
                    email: email.trim(),
                    name: name.trim(),
                    password,
                    role: isProfessor ? 'teacher' : 'student',
                });
            }
            await login(email.trim(), password);
            navigate('/dashboard');
        } catch (err) {
            setError(err.message === 'Failed to fetch'
                ? 'Could not reach the server. Is the backend running on port 8000?'
                : err.message);
        } finally {
            setLoading(false);
        }
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
                        <p className="welcome">Welcome to AI CANVAS</p>
                        <p>Yilmaz</p>
                        <p>This is a barebones login page</p>
                    </div>

                    <form className="input-container" onSubmit={handleSubmit}>
                        <div className="input-fields">
                            {createMode && (
                                <input
                                    type="text"
                                    autoComplete="name"
                                    className="input-box"
                                    placeholder="Full name"
                                    value={name}
                                    onChange={(event) => setName(event.target.value)}
                                />
                            )}
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

                        
                        <button
                            type="submit"
                            className="login"
                            disabled={loading || !email || !password || (createMode && !name.trim())}
                        >
                            {loading ? 'Please wait...' : createMode ? 'Create account' : 'Login'}
                        </button>

                        <label>
                            <input
                                type="checkbox"
                                checked={createMode}
                                onChange={() => { setCreateMode(!createMode); setError(''); }}
                            />
                            Create a new account
                        </label>

                        {createMode && (
                            <label>
                                <input
                                    type="checkbox"
                                    checked={isProfessor}
                                    onChange={() => setIsProfessor(!isProfessor)}
                                />
                                I'm a professor
                            </label>
                        )}
                    </form>
                </div>

                <div className="right-side"></div>
            </div>
        </div>
    </>
    );
}