import { LucideIcon } from 'lucide-react'

export type NavItemKey = 'home' | 'documentation' | 'settings'

export interface NavItem {
  key: NavItemKey
  label: string
  icon: LucideIcon
}

export interface HeaderProps {
  notificationCount: number
  userName?: string
  userAvatar?: string
  activeNavItem: NavItemKey
  onNavigationClick: (item: NavItemKey) => void
  onNotificationClick: () => void
  onProfileClick: () => void
  onMobileMenuClick?: () => void
} 