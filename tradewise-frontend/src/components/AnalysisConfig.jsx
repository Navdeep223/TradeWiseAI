import { useState } from "react";

const BASE_URL = "http://localhost:8000";

function AnalysisConfig({
  selectedHS,
  costPrice,
  setCostPrice,
  mode,
  setMode,
  originCountry,
  setOriginCountry,
  setAnalysisResult,
  setStep
}) {

  const [numContainers, setNumContainers] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {

    if (!costPrice || !mode || !numContainers) {
      setError("Fill all required fields.");
      return;
    }

    if (numContainers < 1) {
      setError("Number of containers must be at least 1.");
      return;
    }

    if (mode === "manual" && !originCountry) {
      setError("Select origin country for manual mode.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${BASE_URL}/analyze-selected-hs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          selected_hs: selectedHS.hs_code,
          destination_country: "India",
          cost_price: parseFloat(costPrice),
          mode: mode,
          num_containers: parseInt(numContainers),
          origin_country: mode === "manual" ? originCountry : null
        })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text);
      }

      const data = await response.json();

      setAnalysisResult(data);
      setStep(4);

    } catch (err) {
      console.error(err);
      setError("Analysis failed.");
    }

    setLoading(false);
  };

  return (
    <div className="space-y-6">

      <button
        onClick={() => setStep(2)}
        className="px-4 py-2 bg-white/10 rounded-lg hover:bg-white/20"
      >
        ← Back
      </button>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleAnalyze();
        }}
        className="bg-white/10 p-6 rounded-xl border border-emerald-400/20 space-y-4"
      >

        <div>
          <label className="block mb-2">Cost Price (Per Container)</label>
          <input
            type="number"
            value={costPrice}
            onChange={(e) => setCostPrice(e.target.value)}
            className="w-full p-3 rounded-lg bg-black/30 border border-emerald-400/30"
          />
        </div>

        <div>
          <label className="block mb-2">Number of Containers</label>
          <input
            type="number"
            min="1"
            value={numContainers}
            onChange={(e) => setNumContainers(e.target.value)}
            className="w-full p-3 rounded-lg bg-black/30 border border-emerald-400/30"
          />
        </div>

        <div>
          <label className="block mb-2">Mode</label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="w-full p-3 rounded-lg bg-black/30 border border-emerald-400/30"
          >
            <option value="">Select Mode</option>
            <option value="ai">AI Optimized</option>
            <option value="manual">Manual Origin</option>
          </select>
        </div>

        {mode === "manual" && (
          <div>
            <label className="block mb-2">Origin Country</label>
            <select
              value={originCountry}
              onChange={(e) => setOriginCountry(e.target.value)}
              className="w-full p-3 rounded-lg bg-black/30 border border-emerald-400/30"
            >
              <option value="">Select Country</option>
              <option>China</option>
              <option>Japan</option>
              <option>Vietnam</option>
              <option>UAE</option>
              <option>Korea</option>
            </select>
          </div>
        )}

        {error && <p className="text-red-400">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-4 bg-emerald-500 rounded-xl font-semibold hover:opacity-90"
        >
          {loading ? "Analyzing..." : "Run Analysis"}
        </button>

      </form>
    </div>
  );
}

export default AnalysisConfig;