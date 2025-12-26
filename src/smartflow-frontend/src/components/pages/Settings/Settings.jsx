import React from 'react';
import './Settings.css';

export function Settings() {
    return (
        <div className="settings-container">
            <div className="settings-section">
                <h2>General Settings</h2>
                <div className="setting-group">
                    <label>Project Name</label>
                    <input type="text" className="settings-input" defaultValue="Smartflow Migration" />
                </div>
                <div className="setting-group">
                    <label>Default Currency</label>
                    <select className="settings-input">
                        <option>USD ($)</option>
                        <option>EUR (€)</option>
                        <option>INR (₹)</option>
                    </select>
                </div>
            </div>

            <div className="settings-section">
                <h2>Notifications</h2>
                <div className="toggle-row">
                    <span>Email Alerts for High Risks</span>
                    <input type="checkbox" defaultChecked />
                </div>
                <div className="toggle-row">
                    <span>Weekly Report Summary</span>
                    <input type="checkbox" defaultChecked />
                </div>
            </div>
        </div>
    );
}