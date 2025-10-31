import React from "react";

const Feature = ({ icon, title, desc, tone }) => (
  <div className={`flex items-start gap-3 p-4 rounded-lg border ${tone.bg} ${tone.border}`}>
    <div className="text-xl" aria-hidden>{icon}</div>
    <div>
      <p className="text-sm font-semibold text-gray-900">{title}</p>
      <p className="text-xs text-gray-600">{desc}</p>
    </div>
  </div>
);

const HeroSection = () => {
  return (
    <section className="py-10">
      <div className="max-w-6xl mx-auto px-4">
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
          <h1 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
            <span className="text-green-600 text-2xl" aria-hidden>🌾</span>
            Welcome to GovData Insight
          </h1>
          <p className="text-sm text-gray-600 mt-2">
            Ask complex questions about India's agricultural economy and climate patterns. Our AI pulls live data from
            <a className="text-blue-600 hover:underline ml-1" href="https://data.gov.in" target="_blank" rel="noreferrer">data.gov.in</a>
            to provide comprehensive insights.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-5">
            <Feature
              icon="📡"
              title="Real-time Data"
              desc="Access live datasets from government portals"
              tone={{ bg: "bg-green-50", border: "border-green-200" }}
            />
            <Feature
              icon="📊"
              title="Deep Analysis"
              desc="Compare trends across states and districts"
              tone={{ bg: "bg-blue-50", border: "border-blue-200" }}
            />
            <Feature
              icon="🤖"
              title="AI-Powered"
              desc="Natural language queries with cited sources"
              tone={{ bg: "bg-cyan-50", border: "border-cyan-200" }}
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
