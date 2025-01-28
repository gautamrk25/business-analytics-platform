import { memo } from 'react'
import { BellIcon, UserIcon } from 'lucide-react'

interface UserControlsProps {
  notificationCount: number
  userName?: string
  userAvatar?: string
  onNotificationClick: () => void
  onProfileClick: () => void
}

export const UserControls = memo(({
  notificationCount,
  userName,
  userAvatar,
  onNotificationClick,
  onProfileClick,
}: UserControlsProps) => {
  const formattedCount = notificationCount > 99 ? '99+' : notificationCount

  return (
    <div className="w-1/4 flex items-center justify-end space-x-4">
      <button
        className="relative p-2 text-white hover:bg-white/10 rounded-lg transition-colors"
        onClick={onNotificationClick}
        aria-label={`${formattedCount} notifications`}
      >
        <BellIcon size={20} />
        {notificationCount > 0 && (
          <span className="absolute -top-2 -right-2 w-5 h-5 flex items-center justify-center bg-red-500 text-white text-xs rounded-full animate-pulse">
            {formattedCount}
          </span>
        )}
      </button>

      <button
        className="flex items-center space-x-2 p-2 text-white hover:bg-white/10 rounded-lg transition-colors"
        onClick={onProfileClick}
        aria-label="User profile"
      >
        {userAvatar ? (
          <img
            src={userAvatar}
            alt={userName || 'User avatar'}
            className="w-5 h-5 rounded-full"
          />
        ) : (
          <UserIcon size={20} />
        )}
        <span className="hidden lg:inline text-sm">{userName || 'User Profile'}</span>
      </button>
    </div>
  )
})

UserControls.displayName = 'UserControls' 