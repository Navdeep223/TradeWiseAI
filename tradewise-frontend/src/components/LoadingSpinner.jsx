import { motion } from "framer-motion";

function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <motion.div
        className="w-14 h-14 border-4 border-blue-500 border-t-transparent rounded-full"
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
      />
      <p className="text-blue-400 text-sm animate-pulse">
        Running intelligent tariff analysis...
      </p>
    </div>
  );
}

export default LoadingSpinner;