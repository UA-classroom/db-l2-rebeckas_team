import React, { useEffect, useState } from "react";
import { apiGet } from "../api";
import BusinessCard from "../components/BusinessCard";

function Businesses() {
    const [businesses, setBusinesses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        apiGet("/businesses/")
            .then(setBusinesses)
            .catch((err) => setError(err.message || "Failed to load"))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="page">
            <header className="page-header">
                <h1>Businesses</h1>
                <p>Browse all businesses available in the platform.</p>
            </header>

            {loading && <p>Loading...</p>}
            {error && <p className="error">{error}</p>}

            <div className="grid">
                {businesses.map((b) => (
                    <BusinessCard key={b.id} business={b} />
                ))}
            </div>
        </div>
    );
}

export default Businesses;
