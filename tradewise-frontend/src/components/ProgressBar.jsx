import { motion } from "framer-motion";

function ProgressBar({ step }) {
  const percentage = ((step - 1) / 3) * 100;

  return (
    <div className="w-full bg-[#0f1626] h-1">
      <motion.div
        className="h-1 bg-gradient-to-r from-blue-500 to-indigo-500"
        initial={{ width: 0 }}
        animate={{ width: `${percentage}%` }}
        transition={{ duration: 0.4 }}
      />
    </div>
  );
}

export default ProgressBar;