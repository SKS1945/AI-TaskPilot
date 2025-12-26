import React, { useState } from 'react';
import { Icons } from '../common/Icons';

export function UserProfile() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="profile-wrapper">
            <div
                className="user-profile"
                onClick={() => setIsOpen(!isOpen)}
                title="User Profile"
            >
                JS
            </div>

            {isOpen && (
                <div className="profile-dropdown-card">
                    <div className="profile-header">
                        <span className="profile-email">john.smith@smartflow.com</span>
                        <div className="profile-avatar-large">JS</div>
                        <div className="profile-greeting">Hi, John!</div>
                        <button className="manage-account-btn">Manage your Account</button>
                    </div>

                    <div className="profile-actions-row">
                        <button className="action-btn-block">
                            <span className="action-icon"><Icons.UserPlus /></span>
                            Add account
                        </button>
                        <button className="action-btn-block">
                            <span className="action-icon"><Icons.LogOut /></span>
                            Sign out
                        </button>
                    </div>

                    <div className="profile-footer-links">
                        <span>Privacy Policy</span> • <span>Terms of Service</span>
                    </div>
                </div>
            )}
        </div>
    );
}