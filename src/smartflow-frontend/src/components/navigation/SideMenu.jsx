import React from 'react';
import { NAV_ITEMS } from './navConfig';

export function SideMenu({ isOpen, onClose, activePage, onNavigate }) {
    return (
        <>
            <div
                className={`drawer-overlay ${isOpen ? 'open' : ''}`}
                onClick={onClose}
            ></div>

            <nav className={`side-menu ${isOpen ? 'open' : ''}`}>
                <div className="menu-header">
                    Smartflow
                </div>
                <ul className="menu-list">
                    {NAV_ITEMS.map((item) => (
                        <li key={item.id}>
                            <div
                                className={`menu-item ${activePage === item.id ? 'active' : ''}`}
                                onClick={() => onNavigate(item.id)}
                            >
                                <span className="menu-icon">{item.icon}</span>
                                <span>{item.label}</span>
                            </div>
                        </li>
                    ))}
                </ul>
            </nav>
        </>
    );
}