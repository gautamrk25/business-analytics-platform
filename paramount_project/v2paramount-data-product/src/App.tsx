import { AppLayout } from './components/Layout/AppLayout';
import { ChecklistPanel } from './components/checklist/ChecklistPanel';
import { ProgressOverview } from './components/Progress/ProgressOverview';
import { ImplementationView } from './components/Implementation/ImplementationView';

function App() {
  return (
    <AppLayout>
      <div className="flex flex-row gap-4 p-4">
        <ChecklistPanel />
        <ProgressOverview />
      </div>
      <ImplementationView />
    </AppLayout>
  );
}

export default App; 