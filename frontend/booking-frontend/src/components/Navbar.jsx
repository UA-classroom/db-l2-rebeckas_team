import React from "react";
import { NavLink } from "react-router-dom";

function Navbar() {
    return (
        <header className="navbar">
            <div className="navbar-inner">
                <NavLink to="/" className="brand">
                    <span className="brand-mark">B</span>
                    <span className="brand-text">Bookable</span>
                </NavLink>

                <nav className="nav-links">
                    <NavLink to="/businesses">Businesses</NavLink>
                    <NavLink to="/categories">Categories</NavLink>
                    {/* Demo customer id = 1 */}
                    <NavLink to="/customers/1/bookings">My bookings</NavLink>
                </nav>
            </div>
        </header>
    );
}

export default Navbar;
