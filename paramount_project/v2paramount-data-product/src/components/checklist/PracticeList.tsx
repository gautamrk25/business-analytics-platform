import { Practice } from '@/types';
import { PracticeCard } from './PracticeCard';
import { motion, AnimatePresence } from 'framer-motion';

interface PracticeListProps {
  practices: Practice[];
  selectedPractices: Set<string>;
  canSelectPractice: (practice: Practice) => boolean;
  onPracticeSelect: (practiceId: string) => void;
}

export function PracticeList({
  practices,
  selectedPractices,
  canSelectPractice,
  onPracticeSelect
}: PracticeListProps) {
  // Group practices by section
  const practicesBySection = practices.reduce((acc, practice) => {
    const section = practice.sectionId;
    if (!acc[section]) {
      acc[section] = [];
    }
    acc[section].push(practice);
    return acc;
  }, {} as Record<string, Practice[]>);

  return (
    <div className="space-y-6">
      {Object.entries(practicesBySection).map(([sectionId, sectionPractices]) => (
        <div key={sectionId} className="space-y-2">
          <h3 className="text-lg font-semibold">{sections[sectionId].title}</h3>
          <AnimatePresence>
            {sectionPractices.map((practice) => (
              <motion.div
                key={practice.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.2 }}
              >
                <PracticeCard
                  practice={practice}
                  isSelected={selectedPractices.has(practice.id)}
                  canSelect={canSelectPractice(practice)}
                  onSelect={() => onPracticeSelect(practice.id)}
                />
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      ))}
    </div>
  );
} 