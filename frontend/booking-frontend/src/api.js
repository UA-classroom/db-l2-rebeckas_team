const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
    const res = await fetch(`${API_BASE_URL}${path}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg || `Request failed with status ${res.status}`);
    }

    // 204 no-content
    if (res.status === 204) return null;

    return res.json();
}

export function apiGet(path) {
    return request(path);
}

export function apiPost(path, body) {
    return request(path, {
        method: "POST",
        body: JSON.stringify(body),
    });
}

export function apiPut(path, body) {
    return request(path, {
        method: "PUT",
        body: JSON.stringify(body),
    });
}

export function apiPatch(path, body) {
    return request(path, {
        method: "PATCH",
        body: JSON.stringify(body),
    });
}

export function apiDelete(path) {
    return request(path, {
        method: "DELETE",
    });
}
