# 🌾 GovData Insight

> An intelligent Q&A system that provides natural language access to Indian agricultural and climate data directly from **data.gov.in**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0-61DAFB?logo=react)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)

## 📋 Overview

**GovData Insight** is an end-to-end prototype of an intelligent question-answering system that sources information directly from the live [data.gov.in](https://data.gov.in) portal of the Indian Government. The system enables users to ask complex, natural language questions about the nation's agricultural economy and its relationship with climate patterns, receiving intelligent, data-driven answers with visualizations and insights.

### Key Features

✨ **Natural Language Processing** - Ask questions in plain English  
🌐 **Live Data Integration** - Direct connection to data.gov.in CKAN API  
📊 **Interactive Visualizations** - Charts and graphs for rainfall and crop data  
🔍 **Intelligent Analysis** - Correlation analysis between rainfall and crop production  
🗺️ **Multi-State Comparison** - Compare agricultural metrics across Indian states  
📈 **Trend Analysis** - Identify patterns and trends in agricultural data  
🎯 **Entity Extraction** - Automatically identifies states, crops, and time periods  
📱 **Modern UI** - Beautiful, responsive chat interface built with React and Tailwind CSS  

## 🏗️ Architecture

```
┌─────────────────┐
│   React Frontend │
│  (Chat Interface)│
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI Backend│
│  (Query Handler) │
└────────┬────────┘
         │
         ├──► Query Parser (Extract entities)
         ├──► Data Fetcher (data.gov.in API)
         ├──► Data Analyzer (Statistical analysis)
         └──► Summarizer (Generate insights)
         │
         ▼
┌─────────────────┐
│   data.gov.in    │
│  (CKAN Datastore)│
└─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP client for API calls
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Data visualization
- **React Chart.js 2** - React wrapper for Chart.js

### Infrastructure
- **Docker** & **Docker Compose** - Containerization
- **Nginx** - Web server for frontend
- **Python 3.11** - Backend runtime

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** (recommended)
- OR **Node.js 18+** and **Python 3.11+** for local development

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Digital_india
   ```

2. **Set environment variables** (Optional, for live data.gov.in access)
   
   **Windows PowerShell:**
   ```powershell
   $env:DATA_GOV_API_KEY="your-api-key-here"
   $env:RAINFALL_RESOURCE_ID="your-rainfall-resource-id"
   $env:CROP_PRODUCTION_RESOURCE_ID="your-crop-resource-id"
   ```
   
   **Linux/Mac:**
   ```bash
   export DATA_GOV_API_KEY="your-api-key-here"
   export RAINFALL_RESOURCE_ID="your-rainfall-resource-id"
   export CROP_PRODUCTION_RESOURCE_ID="your-crop-resource-id"
   ```

   > **Note:** If you don't have API keys, the system will use public export endpoints and fallback to mock data.

3. **Start the application**
   ```bash
   docker compose up --build -d
   ```

4. **Access the application**
   - **Frontend:** http://localhost:5173
   - **Backend API:** http://localhost:8000
   - **API Docs:** http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

```bash
cd frontend
npm install

# Set API URL (PowerShell)
$env:VITE_API_URL="http://localhost:8000"

# Or (Linux/Mac)
export VITE_API_URL="http://localhost:8000"

npm run dev
```

The frontend will be available at http://localhost:5173 (or the port Vite assigns).

## 📚 Configuration

### Environment Variables

#### Backend

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATA_GOV_API_KEY` | API key for data.gov.in CKAN API | No | Uses public endpoints |
| `RAINFALL_RESOURCE_ID` | Resource ID for rainfall dataset | No | Uses export endpoint |
| `CROP_PRODUCTION_RESOURCE_ID` | Resource ID for crop production dataset | No | Uses export endpoint |

#### Frontend

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API base URL | No | `http://127.0.0.1:8000` |

### Getting data.gov.in API Key

1. Visit [data.gov.in](https://data.gov.in)
2. Sign up/Login to your account
3. Navigate to your profile/settings
4. Generate an API key
5. Find the Resource IDs for the datasets you want to use

## 💡 Usage Examples

### Example Queries

The system understands natural language queries about agricultural and climate data:

**Rainfall Queries:**
- "What is the average rainfall in Maharashtra?"
- "Compare rainfall patterns across Karnataka, Kerala, and Tamil Nadu"
- "Show me rainfall trends for the last 5 years"

**Crop Production Queries:**
- "Which states produce the most rice?"
- "Compare wheat production in Punjab and Haryana"
- "What are the top 5 crops by production in Maharashtra?"

**Correlation Analysis:**
- "How does rainfall affect crop production in Karnataka?"
- "What is the relationship between rainfall and rice production?"
- "Analyze the correlation between climate patterns and agricultural output"

**Multi-State Comparison:**
- "Compare agricultural production across Maharashtra, Punjab, and Gujarat"
- "Which state has the best rainfall to crop production ratio?"

### API Usage

#### Query Endpoint

```bash
POST /query
Content-Type: application/json

{
  "query": "Compare rainfall and crop production in Maharashtra and Karnataka"
}
```

**Response:**
```json
{
  "query": "Compare rainfall and crop production in Maharashtra and Karnataka",
  "entities": {
    "states": ["Maharashtra", "Karnataka"],
    "crops": [],
    "years": 5,
    "analysis_type": "comparison"
  },
  "analysis": {
    "rainfall_analysis": [...],
    "crop_analysis": [...],
    "correlation_analysis": {...},
    "state_comparison": [...]
  },
  "summary": "Agricultural analysis for Maharashtra, Karnataka...",
  "citations": [
    "https://data.gov.in/catalog/rainfall-india",
    "https://data.gov.in/catalog/state-wise-season-wise-crop-production-statistics"
  ],
  "data_source": "live"
}
```

## 📁 Project Structure

```
Digital_india/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── Dockerfile             # Backend container config
│   ├── requirements.txt       # Python dependencies
│   └── utils/
│       ├── data_fetcher.py    # Fetches data from data.gov.in
│       ├── data_analyzer.py   # Statistical analysis
│       ├── query_parser.py    # NLP entity extraction
│       └── summarizer.py      # Generates summaries
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React app
│   │   ├── main.jsx           # Entry point
│   │   └── components/
│   │       ├── ChatInterface.jsx      # Chat UI
│   │       ├── HeroSection.jsx        # Landing section
│   │       ├── ExampleQueries.jsx     # Example queries
│   │       ├── InsightCard.jsx        # KPI cards
│   │       └── ...                    # Other components
│   ├── Dockerfile             # Frontend container config
│   ├── nginx.conf             # Nginx configuration
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
├── docker-compose.yml         # Multi-container setup
└── README.md                  # This file
```

## 🔍 How It Works

1. **Query Input** - User submits a natural language question
2. **Entity Extraction** - System parses the query to identify:
   - States (Maharashtra, Punjab, etc.)
   - Crops (Rice, Wheat, etc.)
   - Time periods
   - Analysis type (correlation, trend, comparison, etc.)
3. **Data Fetching** - System fetches data from:
   - Primary: data.gov.in CKAN API (if configured)
   - Fallback: Public export endpoints
   - Final fallback: Mock data for demonstration
4. **Analysis** - Performs statistical analysis:
   - Rainfall statistics by state
   - Crop production metrics
   - Correlation between rainfall and production
   - State-wise comparisons
5. **Summarization** - Generates human-readable insights
6. **Visualization** - Displays charts and graphs
7. **Response** - Returns comprehensive answer with citations

## 🎨 Features in Detail

### Intelligent Query Parsing
- Automatically extracts states, crops, and time periods
- Determines analysis type (correlation, trend, comparison, ranking)
- Handles variations in naming and spelling

### Data Sources
- **Live Integration**: Direct access to data.gov.in via CKAN API
- **Graceful Fallback**: Uses public endpoints if API key not available
- **Mock Data**: Includes sample data for testing without API access

### Analytics Capabilities
- Average, min, max rainfall calculations
- Crop production aggregation and ranking
- Pearson correlation analysis
- Multi-state comparative analysis
- Trend identification

### User Interface
- Modern chat interface with message history
- Interactive charts (Chart.js)
- Key Performance Indicators (KPIs)
- Detailed comparison tables
- Responsive design for mobile and desktop

## 🔧 Development

### Running Tests

```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test
```

### Building for Production

```bash
# Backend (already containerized)
docker build -t govdata-backend ./backend

# Frontend
cd frontend
npm run build
# Output in frontend/dist/
```

### Code Style

- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: ESLint configuration (add if needed)

## 🐛 Troubleshooting

### Backend not connecting to data.gov.in
- Check if `DATA_GOV_API_KEY` is set correctly
- Verify resource IDs are valid
- System will fallback to public endpoints or mock data

### Frontend can't reach backend
- Ensure `VITE_API_URL` points to correct backend URL
- Check CORS settings in `backend/app.py`
- Verify both services are running

### Docker issues
- Ensure Docker and Docker Compose are installed
- Check ports 8000 and 5173 are not in use
- Try `docker compose down` then `docker compose up --build`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **data.gov.in** - For providing open access to Indian government datasets
- **FastAPI** - For the excellent Python web framework
- **React** - For the powerful UI library
- **Tailwind CSS** - For the utility-first CSS framework

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ for Digital India Initiative**

