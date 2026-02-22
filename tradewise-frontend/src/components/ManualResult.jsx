import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  CartesianGrid
} from "recharts";

function ManualResult({ result, setStep }) {

  if (!result || !result.direct_route) {
    return <p className="text-white">No result available.</p>;
  }

  const { direct_route, alternate_routes = [], selected_hs } = result;

  // SAFELY handle route whether string or array
  const formatRoute = (route) => {
    if (!route) return "N/A";
    if (Array.isArray(route)) return route.join(" → ");
    return route; // already string
  };

  // Prepare chart data safely
  const chartData = [
    {
      route: formatRoute(direct_route.route),
      landedCost: direct_route.landing_cost
    },
    ...alternate_routes.map(route => ({
      route: formatRoute(route.route),
      landedCost: route.landing_cost
    }))
  ];

  const bestRoute = chartData.reduce((min, current) =>
    current.landedCost < min.landedCost ? current : min
  );

  return (
    <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden">

      <div className="absolute inset-0 bg-gradient-to-br from-[#062f2a] via-[#0b4f45] to-[#083c35]" />

      <div className="relative z-10 w-[1100px]">

        <div className="bg-white/10 backdrop-blur-3xl border border-white/20 rounded-3xl p-12 shadow-[0_40px_100px_rgba(0,0,0,0.6)]">

          {/* Header */}
          <div className="flex justify-between items-center mb-10">
            <button
              onClick={() => setStep(1)}
              className="px-6 py-2 bg-white/15 border border-white/30 rounded-xl hover:bg-white/25 transition"
            >
              ← Start Over
            </button>

            <h2 className="text-2xl font-semibold text-white">
              Manual Trade Route Comparison
            </h2>

            <div />
          </div>

          {/* Graph */}
          <div className="mb-10">
            <div className="h-[320px] bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-6">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff22" />
                  <XAxis dataKey="route" stroke="#ffffffcc" />
                  <YAxis stroke="#ffffffcc" />
                  <Tooltip />
                  <Bar
                    dataKey="landedCost"
                    fill="#6ee7b7"
                    radius={[10, 10, 0, 0]}
                    animationDuration={1200}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Direct Route */}
          <div className="mb-6 text-white">
            <h3 className="text-lg mb-2 font-semibold text-[#8ff5b0]">
              Direct Route
            </h3>
            <p>Route: {formatRoute(direct_route.route)}</p>
            <p>Total Tariff: {direct_route.total_tariff}%</p>
            <p>Landing Cost: ₹{direct_route.landing_cost}</p>
          </div>

          {/* Alternate Routes */}
          {alternate_routes.length > 0 && (
            <div className="mb-10 text-white">
              <h3 className="text-lg mb-4 font-semibold text-[#8ff5b0]">
                Alternate Routes
              </h3>

              <div className="space-y-4">
                {alternate_routes.map((route, index) => (
                  <div
                    key={index}
                    className="p-5 rounded-2xl bg-white/10 border border-white/20"
                  >
                    <div className="flex justify-between">
                      <span>{formatRoute(route.route)}</span>
                      <span className="text-[#8ff5b0] font-semibold">
                        ₹{route.landing_cost}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Suggested Route */}
          <div className="p-8 rounded-2xl bg-gradient-to-r from-[#0f6d5e] to-[#0c4f44] border border-[#6ee7b7]/40 shadow-lg">

            <h3 className="text-xl text-white mb-4 font-semibold">
              📌 Most Cost Efficient Route
            </h3>

            <p className="text-white text-lg">
              {bestRoute.route}
            </p>

            <p className="text-white text-xl font-bold mt-2">
              Final Landed Cost: ₹{bestRoute.landedCost}
            </p>

          </div>

          <div className="mt-6 text-white/70">
            <p>HS Code: {selected_hs}</p>
          </div>

        </div>
      </div>
    </div>
  );
}

export default ManualResult;