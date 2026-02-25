import { useState, useMemo } from "react";

function SensitivityPanel({
  baseTariff,
  baseFreightPerContainer,
  costPerContainer,
  baseContainers,
  baselineLandedCost
}) {

  const [containers, setContainers] = useState(baseContainers);
  const [tariffDelta, setTariffDelta] = useState(0);
  const [freightDelta, setFreightDelta] = useState(0);

  const simulatedLandedCost = useMemo(() => {

    const goodsValue = costPerContainer * containers;

    const adjustedTariff = baseTariff + tariffDelta;
    const tariffMultiplier = 1 + adjustedTariff / 100;

    const adjustedFreightPerContainer =
      baseFreightPerContainer * (1 + freightDelta / 100);

    const freightTotal = adjustedFreightPerContainer * containers;

    return goodsValue * tariffMultiplier + freightTotal;

  }, [containers, tariffDelta, freightDelta]);

  const deltaPercent =
    ((simulatedLandedCost - baselineLandedCost) /
      baselineLandedCost) * 100;

  return (
    <div className="bg-black/30 p-6 rounded-xl mt-6 space-y-4">

      <h3 className="text-xl font-semibold text-emerald-400">
        Risk Simulation
      </h3>

      {/* Containers */}
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

      {/* Tariff */}
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

      {/* Freight */}
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

      <div className="text-lg font-bold">
        Simulated Landed Cost: ${simulatedLandedCost.toFixed(2)}
      </div>

      <div
        className={`font-semibold ${
          deltaPercent > 0 ? "text-red-400" : "text-emerald-400"
        }`}
      >
        Change: {deltaPercent.toFixed(2)}%
      </div>

    </div>
  );
}

export default SensitivityPanel;