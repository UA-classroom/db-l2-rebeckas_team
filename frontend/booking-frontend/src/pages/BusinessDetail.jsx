import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiGet } from "../api";
import ServiceCard from "../components/ServiceCard";
import RatingStars from "../components/RatingStars";

function BusinessDetail() {
    const { businessId } = useParams();

    const [business, setBusiness] = useState(null);
    const [services, setServices] = useState([]);
    const [reviews, setReviews] = useState([]);
    const [openingHours, setOpeningHours] = useState([]);
    const [rating, setRating] = useState(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function load() {
            try {
                setLoading(true);
                const [b, s, r, oh, rate] = await Promise.all([
                    apiGet(`/businesses/${businessId}`),
                    apiGet(`/businesses/${businessId}/services`),
                    apiGet(`/businesses/${businessId}/reviews`),
                    apiGet(`/businesses/${businessId}/opening-hours`),
                    apiGet(`/businesses/${businessId}/rating`),
                ]);

                setBusiness(b);
                setServices(s);
                setReviews(r);
                setOpeningHours(oh);
                setRating(rate);
            } catch (err) {
                console.error(err);
                setError(err.message || "Failed to load business");
            } finally {
                setLoading(false);
            }
        }

        load();
    }, [businessId]);

    if (loading) return <div className="page"><p>Loading...</p></div>;
    if (error) return <div className="page"><p className="error">{error}</p></div>;
    if (!business) return <div className="page"><p>Business not found</p></div>;

    return (
        <div className="page">
            <header className="page-header">
                <h1>{business.name}</h1>
                <p>{business.description}</p>
                <div className="page-header-meta">
                    <span>{business.city}</span>
                    {rating && (
                        <RatingStars
                            rating={rating.average_rating}
                            count={rating.review_count}
                        />
                    )}
                </div>
            </header>

            <section className="section">
                <h2>Services</h2>
                {services.length === 0 && <p>No services yet.</p>}
                <div className="grid">
                    {services.map((s) => (
                        <ServiceCard key={s.id} service={s} />
                    ))}
                </div>
            </section>

            <section className="section">
                <h2>Opening hours</h2>
                {openingHours.length === 0 && <p>No opening hours configured.</p>}
                <ul className="list">
                    {openingHours.map((oh) => (
                        <li key={oh.id}>
                            <strong>{oh.weekday_name || oh.weekday}</strong>:{" "}
                            {oh.open_time} – {oh.close_time}
                        </li>
                    ))}
                </ul>
            </section>

            <section className="section">
                <h2>Reviews</h2>
                {reviews.length === 0 && <p>No reviews yet.</p>}
                <div className="list">
                    {reviews.map((rev) => (
                        <article key={rev.id} className="card review-card">
                            <header className="review-header">
                                <strong>{rev.author_name || "Anonymous"}</strong>
                                <RatingStars rating={rev.rating} />
                            </header>
                            <p>{rev.comment}</p>
                            <small className="card-meta">
                                {new Date(rev.created_at).toLocaleDateString()}
                            </small>
                        </article>
                    ))}
                </div>
            </section>
        </div>
    );
}

export default BusinessDetail;
