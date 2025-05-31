import { memo } from 'react'
import { NavItem, NavItemKey } from '@/types/navigation'

interface NavButtonProps {
  item: NavItem
  isActive: boolean
  onClick: () => void
}

export const NavButton = memo(({ item, isActive, onClick }: NavButtonProps) => {
  const Icon = item.icon

  return (
    <button
      className={`
        flex flex-col items-center justify-center px-4 py-3 rounded-lg
        text-white transition-colors duration-150
        hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/20
        relative
      `}
      onClick={onClick}
      aria-current={isActive ? 'page' : undefined}
    >
      <Icon size={16} className="mb-1" />
      <span className="text-sm">{item.label}</span>
      {isActive && (
        <div className="absolute bottom-0 left-0 w-full h-0.5 bg-orange-500 transition-transform duration-100 ease-in" />
      )}
    </button>
  )
})

NavButton.displayName = 'NavButton' 