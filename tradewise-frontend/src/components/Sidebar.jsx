import { motion } from "framer-motion";

function Sidebar({ step, setStep }) {

  const steps = [
    "Product",
    "HS Selection",
    "Configuration",
    "Results",
  ];

  return (
    <div className="w-64 bg-[#081a16]/80 backdrop-blur-xl border-r border-white/10 h-screen p-6 flex flex-col justify-between">

      <div>
        <h1 className="text-2xl font-bold text-[#7ee081] mb-12 tracking-wide">
          TradeWise AI
        </h1>

        <div className="space-y-6">
          {steps.map((item, index) => {
            const isActive = step === index + 1;

            return (
              <motion.div
                key={index}
                onClick={() => setStep(index + 1)}
                className={`relative flex items-center gap-4 px-4 py-3 rounded-xl cursor-pointer transition-all duration-300 ${
                  isActive
                    ? "bg-white/10 text-[#7ee081]"
                    : "text-gray-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <div
                  className={`w-6 h-6 flex items-center justify-center rounded-full text-xs font-semibold ${
                    isActive
                      ? "bg-[#7ee081] text-[#06211b]"
                      : "bg-white/10 text-gray-300"
                  }`}
                >
                  {index + 1}
                </div>

                <span className="text-sm font-medium">
                  {item}
                </span>

                {isActive && (
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#7ee081] rounded-r-full"></div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>

      <div className="text-xs text-gray-500">
        Global Trade Intelligence
      </div>

    </div>
  );
}

export default Sidebar;