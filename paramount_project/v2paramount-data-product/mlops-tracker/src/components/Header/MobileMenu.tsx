import { memo } from 'react'
import { NavItem, NavItemKey } from '@/types/navigation'

interface MobileMenuProps {
  isOpen: boolean
  navItems: NavItem[]
  activeNavItem: NavItemKey
  onNavigationClick: (item: NavItemKey) => void
  onClose: () => void
}

export const MobileMenu = memo(({
  isOpen,
  navItems,
  activeNavItem,
  onNavigationClick,
  onClose,
}: MobileMenuProps) => {
  if (!isOpen) return null

  return (
    <div 
      className="fixed inset-0 z-50 md:hidden"
      onClick={onClose}
    >
      <div className="fixed inset-y-0 left-0 w-64 bg-blue-900 shadow-lg transform transition-transform duration-200 ease-in-out">
        <nav className="flex flex-col p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.key}
                className={`
                  flex items-center space-x-3 px-4 py-3 rounded-lg
                  text-white transition-colors duration-150
                  hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/20
                  ${activeNavItem === item.key ? 'bg-white/10' : ''}
                `}
                onClick={() => {
                  onNavigationClick(item.key)
                  onClose()
                }}
                aria-current={activeNavItem === item.key ? 'page' : undefined}
              >
                <Icon size={16} />
                <span>{item.label}</span>
              </button>
            )
          })}
        </nav>
      </div>
    </div>
  )
})

MobileMenu.displayName = 'MobileMenu' 