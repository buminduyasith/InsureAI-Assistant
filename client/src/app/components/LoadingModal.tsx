import React from "react";


interface LoadingModalProps {
    isLoading: boolean;
    message?: string; // Optional message to display
}

const LoadingModal: React.FC<LoadingModalProps> = ({ isLoading, message }) => {
    if (!isLoading) {
        return null;
    }

    return (
        <div
            className="modal show d-block"
            tabIndex={-1}
            style={{
                backgroundColor: "rgba(0, 0, 0, 0.5)",
                pointerEvents: "none", // Prevent interaction with the page
            }}
        >
            <div
                className="modal-dialog modal-dialog-centered"
                style={{ pointerEvents: "auto" }}
            >
                <div className="modal-content bg-transparent border-0">
                    <div className="modal-body text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="sr-only"></span>
                        </div>
                        {message && <p className="mt-3 text-white">{message}</p>}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoadingModal;
