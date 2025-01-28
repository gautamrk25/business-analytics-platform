export function calculateProgress(completed: number, total: number): number {
    return Math.round((completed / total) * 100);
}

export function formatDate(date: Date): string {
    return new Intl.DateTimeFormat('en-US').format(date);
}