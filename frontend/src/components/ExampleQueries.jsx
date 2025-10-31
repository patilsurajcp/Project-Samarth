import React from "react";

const ExampleQueries = ({ setQuery }) => {
  const examples = [
    {
      title: "Compare average annual rainfall in Maharashtra and Punjab for the last 5 years",
      query: "Compare average annual rainfall in Maharashtra and Punjab for the last 5 years",
      icon: "📈"
    },
    {
      title: "What are the top 3 crops produced in Karnataka?",
      query: "What are the top 3 crops produced in Karnataka?",
      icon: "🌾"
    },
    {
      title: "Analyze rice production trends in Tamil Nadu over the last decade",
      query: "Analyze rice production trends in Tamil Nadu over the last decade",
      icon: "📊"
    },
    {
      title: "Which district has the highest wheat production in Uttar Pradesh?",
      query: "Which district has the highest wheat production in Uttar Pradesh?",
      icon: "🗺️"
    }
  ];

  const handleExampleClick = (query) => {
    setQuery(query);
  };

  return (
    <section className="my-8 max-w-3xl mx-auto">
      <div className="bg-white border border-emerald-100 rounded-2xl shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800">Try These Example Questions</h2>
        <div className="mt-4 rounded-lg overflow-hidden border border-emerald-100 divide-y divide-emerald-100 bg-white">
          {examples.map((example, i) => (
            <button
              key={i}
              onClick={() => handleExampleClick(example.query)}
              className="w-full text-left group px-5 py-4 hover:bg-emerald-50 transition"
            >
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="text-xl" aria-hidden>{example.icon}</div>
                  <p className="text-sm text-gray-800 leading-snug">{example.title}</p>
                </div>
                <span className="opacity-0 group-hover:opacity-100 transition text-emerald-600">→</span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ExampleQueries;
