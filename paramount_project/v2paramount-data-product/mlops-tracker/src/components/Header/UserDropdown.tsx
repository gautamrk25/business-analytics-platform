import React, { useState, useRef } from 'react';
import { UserIcon, LogOut, Settings, User } from 'lucide-react';
import { useClickOutside } from '../../hooks/useClickOutside';

interface UserDropdownProps {
  userName?: string;
  userAvatar?: string;
  onProfileClick: () => void;
}

export const UserDropdown: React.FC<UserDropdownProps> = ({
  userName,
  userAvatar,
  onProfileClick,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  useClickOutside(dropdownRef, () => setIsOpen(false));

  return (
    <div ref={dropdownRef} className="relative">
      <button
        className="flex items-center space-x-2 p-2 hover:bg-white/10 rounded-md transition-colors duration-150"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        {userAvatar ? (
          <img
            src={userAvatar}
            alt={userName || 'User avatar'}
            className="w-8 h-8 rounded-full"
          />
        ) : (
          <UserIcon size={20} />
        )}
        <span className="hidden md:inline">{userName || 'User Profile'}</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 top-full mt-1 w-48 py-2 bg-blue-800 rounded-md shadow-lg z-50">
          <button
            className="w-full flex items-center px-4 py-2 text-sm hover:bg-white/10 transition-colors duration-150"
            onClick={onProfileClick}
          >
            <User size={16} className="mr-2" />
            Profile
          </button>
          <button
            className="w-full flex items-center px-4 py-2 text-sm hover:bg-white/10 transition-colors duration-150"
          >
            <Settings size={16} className="mr-2" />
            Settings
          </button>
          <hr className="my-1 border-white/10" />
          <button
            className="w-full flex items-center px-4 py-2 text-sm hover:bg-white/10 transition-colors duration-150"
          >
            <LogOut size={16} className="mr-2" />
            Sign Out
          </button>
        </div>
      )}
    </div>
  );
}; 