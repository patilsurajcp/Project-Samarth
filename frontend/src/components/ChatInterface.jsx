import React, { useState, useRef, useEffect, useMemo } from "react";
import InsightCard from "./InsightCard.jsx";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title
);

const ChatInterface = ({ initialQuery = "" }) => {
  const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showDetails, setShowDetails] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (initialQuery && initialQuery !== query) {
      setQuery(initialQuery);
      // auto-run when example is clicked
      runQuery(initialQuery);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialQuery]);

  const runQuery = async (q) => {
    const finalQuery = q ?? query;
    if (!finalQuery.trim()) return;

    const userMessage = { type: "user", content: finalQuery };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setLoading(true);
    setError("");

    try {
      const res = await fetch(`${API_BASE}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: finalQuery }),
      });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      const assistantMessage = {
        type: "assistant",
        content: data.summary || "No result found.",
        analysis: data.analysis,
        entities: data.entities,
        citations: data.citations,
        dataSource: data.data_source,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setError("Error connecting to the backend. Please try again.");
      const errorMessage = { type: "error", content: `Error: ${error.message}` };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const lastAssistantMessage = useMemo(() => {
    for (let i = messages.length - 1; i >= 0; i -= 1) {
      if (messages[i].type === "assistant") return messages[i];
    }
    return null;
  }, [messages]);

  const rainfallChart = useMemo(() => {
    if (!lastAssistantMessage?.analysis?.rainfall_analysis?.length) return null;
    const ra = lastAssistantMessage.analysis.rainfall_analysis;
    const labels = ra.map((r) => r.State);
    const data = ra.map((r) => r.Average_Rainfall);
    return {
      data: {
        labels,
        datasets: [
          {
            label: "Average Annual Rainfall (mm)",
            data,
            backgroundColor: "rgba(37, 99, 235, 0.6)",
            borderColor: "rgba(37, 99, 235, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          title: { display: true, text: "Rainfall by State" },
        },
        scales: {
          y: { beginAtZero: true },
        },
      },
    };
  }, [lastAssistantMessage]);

  const cropChart = useMemo(() => {
    const ca = lastAssistantMessage?.analysis?.crop_analysis;
    if (!Array.isArray(ca) || ca.length === 0) return null;
    const hasCropColumn = Boolean(ca[0]?.Crop);
    if (!hasCropColumn) return null;

    const sorted = [...ca]
      .sort((a, b) => (b.Production ?? 0) - (a.Production ?? 0))
      .slice(0, 10);
    const labels = sorted.map((c) => `${c.Crop} (${c.State})`);
    const data = sorted.map((c) => c.Production);
    return {
      data: {
        labels,
        datasets: [
          {
            label: "Production (units)",
            data,
            backgroundColor: "rgba(16, 185, 129, 0.6)",
            borderColor: "rgba(16, 185, 129, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          title: { display: true, text: "Top Crops by Production" },
        },
        scales: {
          y: { beginAtZero: true },
        },
      },
    };
  }, [lastAssistantMessage]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    runQuery();
  };

  return (
    <div className="my-8 max-w-5xl mx-auto">
      {/* Chat Messages Container */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-4 h-[30rem] overflow-y-auto border border-gray-200">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-16">
            <div className="text-5xl mb-4">🌾</div>
            <p className="text-lg font-medium">Ask anything about rainfall, crops, and climate</p>
            <p className="text-sm mt-2">Try an example above or use the controls to compose a query.</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`mb-4 ${msg.type === "user" ? "text-right" : ""}`}>
              <div
                className={`inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  msg.type === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : msg.type === "error"
                    ? "bg-red-100 text-red-800 rounded-bl-none"
                    : "bg-gray-100 text-gray-800 rounded-bl-none"
                }`}
              >
                <p className="text-sm">{msg.content}</p>
                {msg.type === "assistant" && msg.dataSource && (
                  <p className="text-xs mt-2 opacity-75">
                    Data source: {msg.dataSource}
                  </p>
                )}
              </div>
              {msg.type === "assistant" && msg.analysis && (
                <div className="mt-2 text-xs text-gray-600 max-w-xs lg:max-w-md">
                  {msg.entities && (
                    <div className="flex flex-wrap gap-2 mb-2">
                      {msg.entities.states?.length ? (
                        <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-50 text-blue-700 border border-blue-200 rounded">
                          <span className="text-[10px] tracking-wide">STATES</span>
                          <span className="font-medium">{msg.entities.states.join(", ")}</span>
                        </span>
                      ) : null}
                      {msg.entities.crops?.length ? (
                        <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-50 text-green-700 border border-green-200 rounded">
                          <span className="text-[10px] tracking-wide">CROPS</span>
                          <span className="font-medium">{msg.entities.crops.join(", ")}</span>
                        </span>
                      ) : null}
                      {typeof msg.entities.years === "number" ? (
                        <span className="inline-flex items-center gap-1 px-2 py-1 bg-amber-50 text-amber-700 border border-amber-200 rounded">
                          <span className="text-[10px] tracking-wide">YEARS</span>
                          <span className="font-medium">{msg.entities.years}</span>
                        </span>
                      ) : null}
                    </div>
                  )}
                  {msg.analysis.correlation_analysis?.correlation !== undefined && msg.analysis.correlation_analysis?.correlation !== null && (
                    <p>📊 Correlation: {msg.analysis.correlation_analysis.correlation}</p>
                  )}
                </div>
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {lastAssistantMessage && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          {rainfallChart && (
            <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
              <Bar data={rainfallChart.data} options={rainfallChart.options} />
            </div>
          )}
          {cropChart && (
            <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
              <Bar data={cropChart.data} options={cropChart.options} />
            </div>
          )}
        </div>
      )}

      {lastAssistantMessage?.analysis?.state_comparison?.length ? (
        <div className="mt-6">
          <button
            type="button"
            className="px-4 py-2 text-sm bg-gray-800 text-white rounded hover:bg-gray-700"
            onClick={() => setShowDetails((v) => !v)}
            aria-expanded={showDetails}
            aria-controls="details-panel"
          >
            {showDetails ? "Hide" : "Show"} Details
          </button>
          {showDetails && (
            <div id="details-panel" className="bg-white rounded-lg shadow p-4 border border-gray-200 mt-3 overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-600">
                    <th className="p-2">State</th>
                    <th className="p-2">Avg Rainfall (mm)</th>
                    <th className="p-2">Min</th>
                    <th className="p-2">Max</th>
                    <th className="p-2">Total Production</th>
                  </tr>
                </thead>
                <tbody>
                  {lastAssistantMessage.analysis.state_comparison.map((row, i) => (
                    <tr key={i} className="border-t">
                      <td className="p-2 font-medium">{row.State}</td>
                      <td className="p-2">{Math.round(row.Average_Rainfall ?? 0)}</td>
                      <td className="p-2">{Math.round(row.Min_Rainfall ?? 0)}</td>
                      <td className="p-2">{Math.round(row.Max_Rainfall ?? 0)}</td>
                      <td className="p-2">{(row.Production ?? 0).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : null}

      {lastAssistantMessage?.citations?.length ? (
        <div className="mt-6 text-sm text-gray-600">
          <p className="font-semibold mb-2">Citations</p>
          <ul className="list-disc list-inside">
            {lastAssistantMessage.citations.map((c, i) => (
              <li key={i}>
                <a className="text-blue-600 hover:underline" href={c} target="_blank" rel="noreferrer">
                  {c}
                </a>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {/* KPIs */}
      {lastAssistantMessage?.analysis ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
          <InsightCard
            title="Avg Rainfall"
            value={(() => {
              const ra = lastAssistantMessage.analysis.rainfall_analysis || [];
              if (!ra.length) return "-";
              const avg = ra.reduce((a, r) => a + (r.Average_Rainfall || 0), 0) / ra.length;
              return `${Math.round(avg)} mm`;
            })()}
            icon="🌧️"
          />
          <InsightCard
            title="Total Production"
            value={(() => {
              const ca = lastAssistantMessage.analysis.crop_analysis || [];
              if (!ca.length) return "-";
              const total = ca.reduce((a, c) => a + (c.Production || 0), 0);
              return total.toLocaleString();
            })()}
            icon="🌾"
          />
          <InsightCard
            title="Correlation"
            value={(() => {
              const corr = lastAssistantMessage.analysis.correlation_analysis?.correlation;
              return corr === null || corr === undefined ? "N/A" : corr;
            })()}
            subtitle={lastAssistantMessage.analysis.correlation_analysis?.interpretation}
            icon="📊"
          />
        </div>
      ) : null}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex items-center gap-2 bg-white border border-gray-200 rounded-full p-2 shadow-sm">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about agricultural production, rainfall, climate patterns..."
          className="flex-1 px-4 py-3 rounded-full focus:outline-none"
          disabled={loading}
          aria-label="Ask a question"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-emerald-600 text-white rounded-full hover:bg-emerald-700 disabled:bg-gray-400 transition"
          aria-label="Send"
          title="Send"
        >
          {loading ? (
            <span className="inline-flex items-center gap-2">
              <span className="inline-block w-4 h-4 border-2 border-white/50 border-t-white rounded-full animate-spin" aria-hidden />
            </span>
          ) : (
            <span className="inline-block" aria-hidden>➤</span>
          )}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-800 rounded-lg text-sm">
          {error}
        </div>
      )}
    </div>
  );
};

export default ChatInterface;
