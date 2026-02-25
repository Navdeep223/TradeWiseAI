import { useState } from "react";

const BASE_URL = "http://localhost:8000";

function Hero({ setRankedHS, setHsExplanation, setStep }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!input.trim()) {
      setError("Please enter a product description.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${BASE_URL}/rank-hs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ description: input }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text);
      }

      const data = await response.json();

      if (!data.ranked_hs_codes || data.ranked_hs_codes.length === 0) {
        throw new Error("No HS codes returned.");
      }

      setRankedHS(data.ranked_hs_codes);
setHsExplanation(data.hs_explanation || ""); 
      setStep(2);
    } catch (err) {
      console.error("ERROR:", err);
      setError("Backend connection failed or invalid endpoint.");
    }

    setLoading(false);
  };

  return (
    <div className="w-full">
      <h2 className="text-5xl font-bold text-white text-center mb-6">
        Verify. Optimize.
        <span className="block text-emerald-400">
          Dominate Trade Flows.
        </span>
      </h2>

      <form
        onSubmit={handleSubmit}
        className="bg-black/30 backdrop-blur-xl border border-emerald-400/20 rounded-2xl p-8 space-y-6"
      >
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your product..."
          rows={4}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();      // Prevent newline
              e.currentTarget.form.requestSubmit();  // Proper form submit
            }
          }}
          className="w-full p-4 rounded-xl bg-white/10 text-white placeholder-emerald-200 border border-emerald-400/30 focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-none"
        />

        {error && (
          <p className="text-red-400 text-sm">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-4 rounded-xl font-semibold text-lg transition-all duration-300 
          bg-gradient-to-r from-emerald-500 to-teal-500 
          hover:scale-[1.02] hover:shadow-lg hover:shadow-emerald-500/40
          disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {loading ? "Analyzing..." : "Initialize Trade Analysis"}
        </button>
      </form>

      <p className="text-center text-emerald-200 text-sm mt-6 opacity-80">
        Powered by AI-driven HS classification and tariff intelligence engine.
      </p>
    </div>
  );
}

export default Hero;