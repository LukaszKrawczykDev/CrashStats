import React from "react";

export default function ChartModal({ isOpen, onClose, title, children }) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center">
            <div className="bg-white rounded-xl w-11/12 h-5/6 p-6 overflow-auto shadow-lg relative">
                <h2 className="text-2xl font-bold mb-4">{title}</h2>
                <button
                    onClick={onClose}
                    className="absolute top-4 right-6 text-gray-600 hover:text-black"
                >
                    Zamknij ✕
                </button>
                {children}
            </div>
        </div>
    );
}