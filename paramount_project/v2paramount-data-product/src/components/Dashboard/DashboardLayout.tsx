import { ChecklistPanel, ProgressPanel, ImplementationPanel } from '@/components';

export function DashboardLayout() {
  return (
    <div className="grid grid-cols-2 gap-6">
      <ChecklistPanel />
      <ProgressPanel />
      <div className="col-span-2">
        <ImplementationPanel />
      </div>
    </div>
  );
} 