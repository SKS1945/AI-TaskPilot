import React from 'react';

export function Placeholder({ pageName }) {
    return (
        <div style={{
            padding: '3rem',
            border: '2px dashed #e2e8f0',
            borderRadius: '12px',
            textAlign: 'center',
            color: '#64748b',
            marginTop: '1rem',
            backgroundColor: '#f8fafc'
        }}>
            <h2 style={{
                fontSize: '1.5rem',
                marginBottom: '0.5rem',
                color: '#0f172a',
                fontWeight: '600'
            }}>
                {pageName}
            </h2>
            <p style={{ fontSize: '0.95rem' }}>
                This module is currently under development.
            </p>
        </div>
    );
}