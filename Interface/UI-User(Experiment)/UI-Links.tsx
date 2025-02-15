import React, { useState } from 'react';
import { IconChevronDown } from '@tabler/icons-react';
import './LinksGroup.css'; // Import CSS for styling

export function LinksGroup({ label, icon: Icon, links }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="links-group">
      {/* Main navigation item */}
      <div className="links-group-header" onClick={() => setOpen(!open)}>
        {Icon && <Icon className="links-group-icon" />}
        <span>{label}</span>
        {links && <IconChevronDown className={`chevron ${open ? 'open' : ''}`} />}
      </div>

      {/* Sub-links (only visible if open) */}
      {links && open && (
        <div className="links-group-dropdown">
          {links.map((link, index) => (
            <a key={index} href={link.link} className="links-group-item">
              {link.label}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
