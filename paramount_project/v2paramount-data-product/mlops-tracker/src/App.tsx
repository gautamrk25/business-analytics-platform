import { ChecklistPanel } from './components/ChecklistPanel/ChecklistPanel';
import { Navigation } from './components/Navigation/Navigation';

function App() {
  return (
    <div className="min-h-screen">
      <Navigation />
      
      <div className="flex pt-[64px]">
        <ChecklistPanel />
        <main className="ml-[25%] flex-1 p-4">
          {/* Your existing routes/content */}
        </main>
      </div>
    </div>
  );
}

export default App;
