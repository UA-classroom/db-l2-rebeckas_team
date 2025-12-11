import React from "react";

function ServiceCard({ service, onSelect }) {
    return (
        <article className="card">
            <h4>{service.name}</h4>
            <p className="card-subtitle">{service.description}</p>
            <p className="card-meta">
                Duration: {service.duration_minutes} min · Price: {service.price} kr
            </p>
            {onSelect && (
                <button className="btn-secondary" onClick={() => onSelect(service)}>
                    Select
                </button>
            )}
        </article>
    );
}

export default ServiceCard;
