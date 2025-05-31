import { LucideIcon } from 'lucide-react';

export type NavItemKey = 'home' | 'documentation' | 'settings';

export interface NavItem {
  key: NavItemKey;
  label: string;
  icon: LucideIcon;
  subItems?: SubNavItem[];
}

export interface SubNavItem {
  key: string;
  label: string;
  href: string;
}

export interface HeaderProps {
  notificationCount: number;
  userName?: string;
  userAvatar?: string;
  activeNavItem: NavItemKey;
  onNavigationClick: (item: NavItemKey) => void;
  onNotificationClick: () => void;
  onProfileClick: () => void;
  onMobileMenuClick?: () => void;
} 