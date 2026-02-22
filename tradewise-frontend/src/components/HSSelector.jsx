import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

function HSSelector({ rankedHS, setSelectedHS, setStep }) {

  // Convert confidence to percentage
  const chartData = rankedHS.map(item => ({
    hs: item.hs_code,
    confidence: Number((item.confidence * 100).toFixed(2)),
    description: item.description
  }));

  const handleSelect = (item) => {
    setSelectedHS(item);
    setStep(3);
  };

  return (
    <div className="w-full">

      <div className="flex items-center justify-between mb-6">
        <button
          onClick={() => setStep(1)}
          className="px-4 py-2 bg-white/10 rounded-lg hover:bg-white/20 transition"
        >
          ← Back
        </button>

        <h2 className="text-3xl font-bold text-white">
          HS Code Confidence Analysis
        </h2>

        <div />
      </div>

      {/* Chart Container */}
      <div className="bg-black/20 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-emerald-400/20">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <XAxis dataKey="hs" stroke="#a7f3d0" />
            <YAxis domain={[0, 100]} stroke="#a7f3d0" />
            <Tooltip />
            <Bar dataKey="confidence" fill="#34d399" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* HS Options */}
      <div className="space-y-4">
        {rankedHS.map((item, index) => (
          <div
            key={index}
            onClick={() => handleSelect(item)}
            className="cursor-pointer bg-white/10 border border-emerald-400/20 rounded-xl p-6 hover:bg-white/20 transition"
          >
            <div className="flex justify-between items-center">
              <div className="text-lg text-white">
                — {item.description}
              </div>
              <div className="text-emerald-400 font-semibold">
                {(item.confidence * 100).toFixed(2)}%
              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}

export default HSSelector;