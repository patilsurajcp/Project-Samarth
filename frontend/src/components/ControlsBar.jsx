import React, { useEffect, useMemo, useState } from "react";

const ControlsBar = ({ onCompose }) => {
  const [states, setStates] = useState("");
  const [crops, setCrops] = useState("");
  const [years, setYears] = useState(5);
  const [live, setLive] = useState(true);

  const composedQuery = useMemo(() => {
    const s = states.trim();
    const c = crops.trim();
    const y = Number(years) || 5;
    const statesPart = s ? ` in ${s}` : " across all major states";
    const cropsPart = c ? ` focusing on ${c}` : "";
    return `Analyze rainfall and crop production${statesPart}${cropsPart} for the last ${y} years and report correlations.`;
  }, [states, crops, years]);

  useEffect(() => {
    if (live && onCompose) {
      const id = setTimeout(() => onCompose(composedQuery), 600);
      return () => clearTimeout(id);
    }
  }, [composedQuery, live, onCompose]);

  return (
    <div className="bg-white rounded-lg shadow p-4 border border-gray-200 mb-4">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3 items-end">
        <div>
          <label className="block text-xs text-gray-600 mb-1">States (comma-separated)</label>
          <input
            value={states}
            onChange={(e) => setStates(e.target.value)}
            className="w-full border border-gray-300 p-2 rounded"
            placeholder="Maharashtra, Gujarat"
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Crops (comma-separated)</label>
          <input
            value={crops}
            onChange={(e) => setCrops(e.target.value)}
            className="w-full border border-gray-300 p-2 rounded"
            placeholder="Wheat, Rice"
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Years (N)</label>
          <input
            type="number"
            min={1}
            max={20}
            value={years}
            onChange={(e) => setYears(e.target.value)}
            className="w-full border border-gray-300 p-2 rounded"
          />
        </div>
        <div className="flex items-center gap-3">
          <button
            type="button"
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            onClick={() => onCompose && onCompose(composedQuery)}
          >
            Run
          </button>
          <label className="inline-flex items-center gap-2 text-sm text-gray-700">
            <input type="checkbox" checked={live} onChange={(e) => setLive(e.target.checked)} />
            Live
          </label>
        </div>
      </div>
      <p className="text-xs text-gray-500 mt-2">Query preview: <span className="italic">{composedQuery}</span></p>
    </div>
  );
};

export default ControlsBar;


