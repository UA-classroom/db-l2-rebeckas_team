import React from "react";

function Footer() {
    return (
        <footer className="footer">
            <span>© {new Date().getFullYear()} Bookable Platform</span>
            <span className="footer-secondary">
                Built with FastAPI & React
            </span>
        </footer>
    );
}

export default Footer;
