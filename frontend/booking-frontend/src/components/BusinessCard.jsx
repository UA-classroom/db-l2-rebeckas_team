import React from "react";
import { Link } from "react-router-dom";
import RatingStars from "./RatingStars";

function BusinessCard({ business }) {
    return (
        <article className="card">
            <div className="card-header">
                <h3>{business.name}</h3>
                {business.rating && (
                    <RatingStars rating={business.rating} count={business.review_count} />
                )}
            </div>
            <p className="card-subtitle">{business.description}</p>
            <p className="card-meta">
                {business.city && <span>{business.city}</span>}
                {business.phone && <span> · {business.phone}</span>}
            </p>
            <div className="card-actions">
                <Link to={`/businesses/${business.id}`} className="btn-primary">
                    View details
                </Link>
            </div>
        </article>
    );
}

export default BusinessCard;
