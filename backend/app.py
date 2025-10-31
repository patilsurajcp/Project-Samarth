from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from utils import query_parser, data_fetcher, data_analyzer, summarizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GovData Insight API",
    description="Intelligent Q&A system for Indian agricultural data from data.gov.in",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": "GovData Insight API Running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "GovData Insight API",
        "features": [
            "Natural language query processing",
            "Live data.gov.in integration",
            "Rainfall-crop correlation analysis",
            "Multi-state agricultural comparison"
        ]
    }

@app.post("/query")
async def handle_query(request: Request):
    """
    Process natural language queries about Indian agricultural data.

    Request body:
    {
        "query": "Your question about agricultural data"
    }

    Returns:
    {
        "query": "Original query",
        "entities": {"states": [...], "crops": [...], "years": ..., "analysis_type": "..."},
        "analysis": {...},
        "summary": "Human-readable summary",
        "citations": [...],
        "data_source": "live or mock"
    }
    """
    try:
        data = await request.json()
        query = data.get("query", "").strip()

        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        logger.info(f"Processing query: {query}")

        # Step 1: Parse entities (state, crop, years, analysis_type)
        entities = query_parser.extract_entities(query)
        logger.info(f"Extracted entities: {entities}")

        # Step 2: Fetch data (live + mock fallback)
        datasets = data_fetcher.fetch_data(entities)
        logger.info(f"Data source: {datasets.get('data_source', 'unknown')}")

        # Step 3: Analyze data
        analysis_result = data_analyzer.perform_analysis(datasets, entities)

        # Step 4: Summarize and format output
        summary = summarizer.generate_summary(analysis_result, query)

        return {
            "query": query,
            "entities": entities,
            "analysis": analysis_result,
            "summary": summary,
            "citations": datasets["sources"],
            "data_source": datasets.get("data_source", "mock")
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
