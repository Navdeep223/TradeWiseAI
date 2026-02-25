import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  CartesianGrid,
  Cell
} from "recharts";
import { useState, useMemo } from "react";

function AIResult({ result, setStep }) {

  if (!result) {
    return <p className="text-white">No result available.</p>;
  }

  const {
    recommended_origin,
    final_tariff_percent,
    estimated_landing_cost,
    spread_percent,
    arbitrage_level,
    comparison_table,
    selected_hs
  } = result;

  const baseContainers = 1;
  const baseFreightPerContainer =
    (result.freight_cost_usd ?? 0) / baseContainers;

  const baseCostPerContainer =
    (estimated_landing_cost - (result.freight_cost_usd ?? 0)) /
    (1 + final_tariff_percent / 100);

  const [containers, setContainers] = useState(baseContainers);
  const [tariffDelta, setTariffDelta] = useState(0);
  const [freightDelta, setFreightDelta] = useState(0);

  const simulatedCost = useMemo(() => {

    const goodsValue = baseCostPerContainer * containers;

    const adjustedTariff =
      final_tariff_percent + tariffDelta;

    const tariffMultiplier = 1 + adjustedTariff / 100;

    const adjustedFreight =
      baseFreightPerContainer * (1 + freightDelta / 100);

    const freightTotal = adjustedFreight * containers;

    return goodsValue * tariffMultiplier + freightTotal;

  }, [containers, tariffDelta, freightDelta]);

  const deltaPercent =
    ((simulatedCost - estimated_landing_cost) /
      estimated_landing_cost) * 100;

  // ================================
  // RISK FACTOR LOGIC (ONLY ADDITION)
  // ================================

  const chartData = (comparison_table || []).map(item => {

    const tariffComponent =
      Math.pow(item.tariff_percent / 25, 1.3);

    const freightComponent =
      (item.freight_cost_usd ?? 0) /
      (item.landed_cost ?? 1);

    const hopPenalty =
      item.country !== recommended_origin ? 0.08 : 0;

    let riskScore =
      (tariffComponent * 0.65) +
      (freightComponent * 0.25) +
      hopPenalty;

    riskScore = Math.min(riskScore * 100, 100);

    let color = "#6ee7b7";
    if (riskScore > 65) color = "#ef4444";
    else if (riskScore > 35) color = "#facc15";

    return {
      country: item.country,
      landedCost: item.landed_cost ?? 0,
      riskScore: riskScore.toFixed(1),
      fill: color
    };
  });

  return (
    <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-[#062f2a] via-[#0b4f45] to-[#083c35]" />

      <div className="relative z-10 w-[1100px]">
        <div className="bg-white/10 backdrop-blur-3xl border border-white/20 rounded-3xl p-12 shadow-[0_40px_100px_rgba(0,0,0,0.6)]">

          <div className="flex justify-between items-center mb-10">
            <button
              onClick={() => setStep(1)}
              className="px-6 py-2 bg-white/15 border border-white/30 rounded-xl hover:bg-white/25 transition"
            >
              ← Start Over
            </button>

            <h2 className="text-2xl font-semibold text-white">
              AI Optimized Trade Route
            </h2>

            <div />
          </div>

          {/* Recommendation Block (UNCHANGED) */}
          <div className="mb-10 p-8 rounded-2xl bg-gradient-to-r from-[#0f6d5e] to-[#0c4f44] border border-[#6ee7b7]/40 shadow-lg">

            <h3 className="text-xl text-white mb-4 font-semibold">
              🚀 Recommended Origin
            </h3>

            <p className="text-white text-lg">
              Country: <span className="text-[#8ff5b0] font-semibold">{recommended_origin}</span>
            </p>

            <p className="text-white text-lg">
              Final Tariff: <span className="text-[#8ff5b0]">{final_tariff_percent}%</span>
            </p>

            <p className="text-white text-lg">
              Freight Cost: ₹{result.freight_cost_usd ?? 0}
            </p>

            <p className="text-white text-xl font-bold mt-2">
              Estimated Landing Cost: ₹{estimated_landing_cost}
            </p>

            <p className="text-white mt-2">
              Spread: {spread_percent}%
            </p>

            <p className="text-white">
              Arbitrage Level: <span className="text-[#8ff5b0]">{arbitrage_level}</span>
            </p>

          </div>

          {/* Sensitivity Panel (UNCHANGED) */}
          <div className="bg-black/30 p-6 rounded-2xl mb-10 space-y-4">
            <h3 className="text-lg font-semibold text-emerald-400">
              🔬 Real-Time Sensitivity Analysis
            </h3>

            <div>
              <label>Containers: {containers}</label>
              <input
                type="range"
                min="1"
                max="50"
                value={containers}
                onChange={(e) => setContainers(parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label>Tariff Adjustment: {tariffDelta}%</label>
              <input
                type="range"
                min="-20"
                max="20"
                value={tariffDelta}
                onChange={(e) => setTariffDelta(parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label>Freight Adjustment: {freightDelta}%</label>
              <input
                type="range"
                min="-30"
                max="30"
                value={freightDelta}
                onChange={(e) => setFreightDelta(parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            <div className="text-xl font-bold text-white">
              Simulated Cost: ₹{simulatedCost.toFixed(2)}
            </div>

            <div className={`font-semibold ${deltaPercent > 0 ? "text-red-400" : "text-emerald-400"}`}>
              Change from Baseline: {deltaPercent.toFixed(2)}%
            </div>
          </div>

          {/* Graph with Risk Coloring */}
          {chartData.length > 0 && (
            <>
              <div className="h-[350px] bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-6">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff22" />
                    <XAxis dataKey="country" stroke="#ffffffcc" />
                    <YAxis stroke="#ffffffcc" />
                    <Tooltip
                      cursor={{ fill: "transparent" }}
                      formatter={(value, name, props) => [
                        `₹${value}`,
                        `Risk: ${props.payload.riskScore}`
                      ]}
                      contentStyle={{
                        backgroundColor: "#062f2a",
                        border: "1px solid #6ee7b7",
                        borderRadius: "10px",
                        color: "white"
                      }}
                    />
                    <Bar dataKey="landedCost" radius={[10, 10, 0, 0]} animationDuration={1200}>
                      {chartData.map((entry, index) => (
                        <Cell key={index} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Risk Legend */}
              <div className="mt-6 text-white space-y-2">
                <div className="flex items-center gap-3">
                  <div className="w-4 h-4 bg-[#6ee7b7] rounded"></div>
                  <span>Low Risk (0–35)</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-4 h-4 bg-[#facc15] rounded"></div>
                  <span>Moderate Risk (35–65)</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-4 h-4 bg-[#ef4444] rounded"></div>
                  <span>High Risk (65+)</span>
                </div>
              </div>
            </>
          )}
          {/* ================================
   LLM EXPLANATION SECTION
================================ */}

{result.explanation && (
  <div className="mt-10 bg-black/30 p-6 rounded-2xl border border-emerald-400/30">
    <h3 className="text-xl font-semibold text-emerald-400 mb-4">
      🧠 AI Trade Insight
    </h3>

    <div className="text-white whitespace-pre-line leading-relaxed">
      {result.explanation}
    </div>
  </div>
)}
          <div className="mt-8 text-white/80">
            <p>HS Code: {selected_hs}</p>
          </div>

        </div>
      </div>
    </div>
  );
}

export default AIResult;