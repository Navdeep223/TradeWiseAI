import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  CartesianGrid
} from "recharts";

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

  // 🔥 Normalize comparison table safely
  const chartData = (comparison_table || []).map(item => ({
    country: item.country,
    tariff:
      item.tariff_percent ??
      item.total_tariff ??
      item.tariff ??
      0
  }));

  return (
    <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden">

      <div className="absolute inset-0 bg-gradient-to-br from-[#062f2a] via-[#0b4f45] to-[#083c35]" />

      <div className="relative z-10 w-[1100px]">

        <div className="bg-white/10 backdrop-blur-3xl border border-white/20 rounded-3xl p-12 shadow-[0_40px_100px_rgba(0,0,0,0.6)]">

          {/* HEADER */}
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

          {/* BEST ROUTE */}
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

          {/* GRAPH */}
          {chartData.length > 0 && (
            <div className="h-[350px] bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-6">

              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff22" />
                  <XAxis dataKey="country" stroke="#ffffffcc" />
                  <YAxis domain={[0, "auto"]} stroke="#ffffffcc" />
                  <Tooltip />
                  <Bar
                    dataKey="tariff"
                    fill="#6ee7b7"
                    radius={[10, 10, 0, 0]}
                    animationDuration={1200}
                  />
                </BarChart>
              </ResponsiveContainer>

            </div>
          )}

          {/* SUMMARY */}
          <div className="mt-8 text-white/80">
            <p>HS Code: {selected_hs}</p>
          </div>

        </div>
      </div>
    </div>
  );
}

export default AIResult;