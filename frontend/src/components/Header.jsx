import React from "react";

const Header = () => {
  return (
    <header className="w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center gap-3">
          <div className="text-3xl" aria-hidden>🗃️✨</div>
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">GovData Insight</h1>
            <p className="text-sm text-gray-600">AI-Powered Agricultural & Climate Data Analysis</p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;


