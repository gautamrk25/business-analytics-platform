import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMLOpsStore } from '@/store';
import { 
  AnimatedProgress, 
  CodeEditor, 
  ResourcePanel 
} from '@/components';

export function ImplementationCard({ practiceId }: { practiceId: string }) {
  const [showCode, setShowCode] = useState(false);
  const practice = useMLOpsStore((state) => state.practices[practiceId]);
  const implementation = useMLOpsStore((state) => state.implementations[practiceId]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-lg p-6"
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">{practice.name}</h3>
        <span className="badge badge-primary">{implementation.status}</span>
      </div>

      <div className="space-y-4">
        {/* Progress Phases */}
        {Object.entries(implementation.phases).map(([phase, state]) => (
          <div key={phase} className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm font-medium">{phase}</span>
              <span className="text-sm text-gray-500">{state.progress}%</span>
            </div>
            <AnimatedProgress progress={state.progress} />
          </div>
        ))}

        {/* Action Buttons */}
        <div className="flex space-x-3 mt-4">
          <button
            onClick={() => setShowCode(true)}
            className="btn btn-primary btn-sm"
          >
            View Code
          </button>
          <button className="btn btn-outline btn-sm">
            View Resources
          </button>
        </div>
      </div>

      {/* Code Editor Modal */}
      <AnimatePresence>
        {showCode && (
          <CodeEditor
            code={practice.code.current}
            language={practice.code.language}
            onClose={() => setShowCode(false)}
            onSave={(newCode) => {
              // Handle code save
            }}
          />
        )}
      </AnimatePresence>
    </motion.div>
  );
} 