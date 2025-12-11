import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiGet } from "../api";

function Bookings() {
    const { customerId } = useParams();
    const [upcoming, setUpcoming] = useState([]);
    const [past, setPast] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function load() {
            try {
                setLoading(true);
                const [u, p] = await Promise.all([
                    apiGet(`/customers/${customerId}/bookings/upcoming`),
                    apiGet(`/customers/${customerId}/bookings/past`),
                ]);
                setUpcoming(u);
                setPast(p);
            } catch (err) {
                setError(err.message || "Failed to load bookings");
            } finally {
                setLoading(false);
            }
        }
        load();
    }, [customerId]);

    const renderBooking = (b) => (
        <article key={b.id} className="card">
            <h3>Booking #{b.id}</h3>
            <p className="card-meta">
                {new Date(b.starttime).toLocaleString()} –{" "}
                {new Date(b.endtime).toLocaleString()}
            </p>
            <p>Status: {b.status}</p>
            <p>Business ID: {b.business_id} · Service ID: {b.service_id}</p>
        </article>
    );

    return (
        <div className="page">
            <header className="page-header">
                <h1>My bookings</h1>
                <p>Customer #{customerId}</p>
            </header>

            {loading && <p>Loading...</p>}
            {error && <p className="error">{error}</p>}

            <section className="section">
                <h2>Upcoming</h2>
                {upcoming.length === 0 && <p>No upcoming bookings.</p>}
                <div className="grid">{upcoming.map(renderBooking)}</div>
            </section>

            <section className="section">
                <h2>Past</h2>
                {past.length === 0 && <p>No previous bookings.</p>}
                <div className="grid">{past.map(renderBooking)}</div>
            </section>
        </div>
    );
}

export default Bookings;
