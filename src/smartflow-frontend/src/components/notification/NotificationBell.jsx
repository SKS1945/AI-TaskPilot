import React from 'react';
import { Icons } from '../common/Icons';

export function NotificationBell() {
    return (
        <button className="icon-btn" title="Notifications">
            <Icons.Bell />
            <span className="badge"></span>
        </button>
    );
}