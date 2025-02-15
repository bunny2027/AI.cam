import React from 'react';
import './NavbarButtons.css'; // Import the CSS for styling

export function UserButton({ label, icon: Icon, onClick, isActive }) {
  return (
    <button className={`navbar-button ${isActive ? 'active' : ''}`} onClick={onClick}>
      {Icon && <Icon className="navbar-button-icon" />}
      <span>{label}</span>
    </button>
  );
}
