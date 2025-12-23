import { useState } from 'react';

const SideMenu = ({ isOpen, items, onClose }) => {
    const [expandedItems, setExpandedItems] = useState(new Set(['timeline']));

    const toggleItem = (id) => {
        const newExpanded = new Set(expandedItems);
        if (newExpanded.has(id)) {
            newExpanded.delete(id);
        } else {
            newExpanded.add(id);
        }
        setExpandedItems(newExpanded);
    };

    const handleItemClick = (e, hasChildren) => {
        if (hasChildren) {
            e.preventDefault();
            toggleItem(e.currentTarget.dataset.id);
        }
        if (window.innerWidth < 768) {
            onClose();
        }
    };

    return (
        <div className={`side-menu ${isOpen ? 'open' : ''}`}>
            <div className="menu-header">
                <h1 className="app-logo">Smartflow</h1>
                <button
                    className="close-menu"
                    onClick={onClose}
                    aria-label="Close menu"
                >
                    ✕
                </button>
            </div>

            <nav className="menu-content">
                <ul>
                    {items.map(item => (
                        <li key={item.id} className="menu-item">
                            <a
                                href={`#${item.id}`}
                                className={`menu-link ${expandedItems.has(item.id) ? 'expanded' : ''}`}
                                data-id={item.id}
                                onClick={(e) => handleItemClick(e, item.children)}
                            >
                                <span className="menu-icon">{item.icon}</span>
                                <span className="menu-label">{item.label}</span>
                                {item.children && (
                                    <span className="submenu-toggle">
                    {expandedItems.has(item.id) ? '▴' : '▾'}
                  </span>
                                )}
                            </a>

                            {item.children && expandedItems.has(item.id) && (
                                <ul className="submenu">
                                    {item.children.map(child => (
                                        <li key={child.id} className="submenu-item">
                                            <a href={`#${child.id}`} className="submenu-link">
                                                {child.label}
                                            </a>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </li>
                    ))}
                </ul>
            </nav>

            <div className="menu-footer">
                <div className="workflow-indicator">
                    <span>Workflow:</span>
                    <span className="workflow-steps">plan → assign → execute → monitor → predict → report → act</span>
                </div>
            </div>
        </div>
    );
};

export default SideMenu;