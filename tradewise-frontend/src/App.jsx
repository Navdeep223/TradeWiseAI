import { useState } from "react";

import Hero from "./components/Hero";
import HSSelector from "./components/HSSelector";
import AnalysisConfig from "./components/AnalysisConfig";
import AIResult from "./components/AIResult";
import ManualResult from "./components/ManualResult";
import Sidebar from "./components/Sidebar";

function App() {
  const [step, setStep] = useState(1);

  // Step 1
  const [rankedHS, setRankedHS] = useState([]);

  // Step 2
  const [selectedHS, setSelectedHS] = useState(null);

  // Step 3
  const [costPrice, setCostPrice] = useState("");
  const [mode, setMode] = useState(""); // "manual" or "ai"
  const [originCountry, setOriginCountry] = useState("");

  // Step 4
  const [analysisResult, setAnalysisResult] = useState(null);

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-[#042f2e] via-[#064e3b] to-[#022c22]">

      {/* Sidebar */}
      <Sidebar step={step} />

      {/* Main Content */}
      <div className="flex-1 p-10 flex justify-center items-start">
        <div className="w-full max-w-6xl bg-black/30 backdrop-blur-xl border border-emerald-400/20 rounded-2xl shadow-2xl p-8 text-white">

          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-emerald-300">
              TradeWise AI
            </h1>
            <p className="mt-2 text-emerald-200 max-w-2xl">
              AI-powered tariff intelligence system that analyzes HS classification,
              compares global duty structures, and recommends optimal sourcing routes
              based on landed cost simulation.
            </p>
          </div>

          {/* STEP 1 — Rank HS */}
          {step === 1 && (
            <Hero
              setRankedHS={setRankedHS}
              setStep={setStep}
            />
          )}

          {/* STEP 2 — Select HS */}
          {step === 2 && (
            <HSSelector
              rankedHS={rankedHS}
              setSelectedHS={setSelectedHS}
              setStep={setStep}
            />
          )}

          {/* STEP 3 — Configure Analysis */}
          {step === 3 && (
            <AnalysisConfig
              selectedHS={selectedHS}
              costPrice={costPrice}
              setCostPrice={setCostPrice}
              mode={mode}
              setMode={setMode}
              originCountry={originCountry}
              setOriginCountry={setOriginCountry}
              setAnalysisResult={setAnalysisResult}
              setStep={setStep}
            />
          )}

          {/* STEP 4 — AI Result */}
          {step === 4 && mode === "ai" && (
            <AIResult
              result={analysisResult}
              setStep={setStep}
            />
          )}

          {/* STEP 4 — Manual Result */}
          {step === 4 && mode === "manual" && (
            <ManualResult
              result={analysisResult}
              setStep={setStep}
            />
          )}

        </div>
      </div>
    </div>
  );
}

export default App;