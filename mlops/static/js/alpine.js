document.addEventListener('alpine:init', () => {
    Alpine.data('notificationSystem', () => ({
        notifications: [],
        add(notification) {
            const id = Date.now();
            notification.id = id;
            notification.visible = true;
            
            this.notifications.push(notification);

            // Auto remove after duration (default 5000ms)
            setTimeout(() => {
                this.remove(id);
            }, notification.duration || 5000);
        },
        remove(id) {
            const notification = this.notifications.find(n => n.id === id);
            if (notification) {
                notification.visible = false;
                setTimeout(() => {
                    this.notifications = this.notifications.filter(n => n.id !== id);
                }, 300);
            }
        }
    }));
});
