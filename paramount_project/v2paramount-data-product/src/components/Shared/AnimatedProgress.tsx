import { motion } from 'framer-motion';

export function AnimatedProgress({ progress }: { progress: number }) {
  return (
    <div className="relative h-2 bg-gray-200 rounded-full overflow-hidden">
      <motion.div
        className="absolute h-full bg-blue-500 rounded-full"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      />
    </div>
  );
} 