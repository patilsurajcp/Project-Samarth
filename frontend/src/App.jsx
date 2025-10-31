import React, { useState } from "react";
import HeroSection from "./components/HeroSection.jsx";
import Header from "./components/Header.jsx";
import ExampleQueries from "./components/ExampleQueries.jsx";
import ChatInterface from "./components/ChatInterface.jsx";

export default function App() {
  const [query, setQuery] = useState("");

  return (
    <div className="min-h-screen bg-emerald-50 text-gray-800 relative">
      <Header />
      <HeroSection />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <ExampleQueries setQuery={setQuery} />
        <ChatInterface initialQuery={query} />
      </div>
      <footer className="mt-12 py-6 bg-gray-800 text-white text-center">
        <p className="text-sm">
          Data sourced from{" "}
          <a
            href="https://data.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-300"
          >
            data.gov.in
          </a>
          {" "}- Government of India's Open Data Portal
        </p>
      </footer>
    </div>
  );
}
