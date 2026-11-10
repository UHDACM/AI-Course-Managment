export const API_URL = "http://localhost:8000";
const TOKEN_KEY = "access_token";

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export function clearToken() {
  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch {
    /* ignore */
  }
}

async function errorMessage(response) {
  try {
    const data = await response.json();
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail) && data.detail[0]?.msg) return data.detail[0].msg;
  } catch {
    /* fall through */
  }
  return `Request failed (${response.status})`;
}

export async function register({ email, name, password, role }) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, name, password, role }),
  });
  if (!response.ok) throw new Error(await errorMessage(response));
  return response.json();
}

// /auth/login uses OAuth2PasswordRequestForm: form-encoded, field "username" holds the email.
export async function login(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username: email, password }),
  });
  if (!response.ok) throw new Error(await errorMessage(response));
  const data = await response.json();
  try {
    localStorage.setItem(TOKEN_KEY, data.access_token);
  } catch {
    /* ignore */
  }
  return data;
}
