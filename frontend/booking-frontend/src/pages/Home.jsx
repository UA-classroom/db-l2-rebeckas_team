import React, { useEffect, useState } from "react";
import { apiGet } from "../api";
import BusinessCard from "../components/BusinessCard";
import { Link } from "react-router-dom";

function Home() {
    const [topBusinesses, setTopBusinesses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        apiGet("/businesses/top-rated?limit=4")
            .then(setTopBusinesses)
            .catch((err) => setError(err.message || "Failed to load"))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="page">
            <section className="hero">
                <div className="hero-text">
                    <h1>Book services you love, effortlessly.</h1>
                    <p>
                        A modern booking platform powered by FastAPI and React.
                        Discover businesses, explore services, and manage your bookings
                        in one place.
                    </p>
                    <div className="hero-actions">
                        <Link to="/businesses" className="btn-primary">
                            Browse businesses
                        </Link>
                        <Link to="/categories" className="btn-secondary">
                            Explore categories
                        </Link>
                    </div>
                </div>
                <div className="hero-panel">
                    <h2>Top rated businesses</h2>
                    {loading && <p>Loading...</p>}
                    {error && <p className="error">{error}</p>}
                    {!loading && !error && topBusinesses.length === 0 && (
                        <p>No businesses yet.</p>
                    )}
                    <div className="grid">
                        {topBusinesses.map((b) => (
                            <BusinessCard key={b.id} business={b} />
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Home;
