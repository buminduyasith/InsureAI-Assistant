'use client';
import React from 'react';
import { useRouter } from 'next/navigation';

const Navbar = () => {
    const router = useRouter();

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        router.push('/');
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container-fluid">
                <a className="navbar-brand" href="/">
                    AI Insurance Navigator
                </a>
                <div className="d-flex align-items-center">
                    <button
                        className="btn btn-outline-warning"
                        onClick={handleLogout}
                        title="Logout"
                    >
                        Sign out
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
