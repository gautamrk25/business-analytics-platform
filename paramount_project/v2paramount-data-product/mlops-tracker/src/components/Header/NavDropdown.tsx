import React, { useRef } from 'react';
import { NavItem } from './types';
import { useClickOutside } from '../../hooks/useClickOutside';

interface NavDropdownProps {
  item: NavItem;
  isActive: boolean;
  isOpen: boolean;
  onOpen: () => void;
  onClose: () => void;
  onClick: () => void;
}

export const NavDropdown: React.FC<NavDropdownProps> = ({
  item,
  isActive,
  isOpen,
  onOpen,
  onClose,
  onClick,
}) => {
  const dropdownRef = useRef<HTMLDivElement>(null);
  useClickOutside(dropdownRef, onClose);

  const Icon = item.icon;

  return (
    <div ref={dropdownRef} className="relative">
      <button
        className={`
          flex flex-col items-center px-4 py-3 rounded-md
          hover:bg-white/10 transition-colors duration-150
          focus:outline-none focus:ring-2 focus:ring-white/20
          ${isActive ? 'border-b-2 border-orange-500' : ''}
        `}
        onClick={() => {
          onClick();
          if (item.subItems?.length) {
            isOpen ? onClose() : onOpen();
          }
        }}
        onMouseEnter={() => item.subItems?.length && onOpen()}
        aria-current={isActive ? 'page' : undefined}
        aria-expanded={isOpen}
      >
        <Icon size={16} className="mb-1" />
        <span className="text-sm">{item.label}</span>
      </button>

      {isOpen && item.subItems && (
        <div
          className="
            absolute top-full left-0 mt-1 py-2
            bg-blue-800 rounded-md shadow-lg
            min-w-[200px] z-50
          "
        >
          {item.subItems.map((subItem) => (
            <a
              key={subItem.key}
              href={subItem.href}
              className="
                block px-4 py-2 text-sm
                hover:bg-white/10 transition-colors duration-150
              "
            >
              {subItem.label}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}; 