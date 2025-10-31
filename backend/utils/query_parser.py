import re

def extract_entities(query: str):
    """
    Extract entities (states, crops, years, analysis_type) from a natural language query.

    Args:
        query: Natural language query string

    Returns:
        Dictionary with extracted states, crops, years, and analysis type
    """
    # Convert query to lowercase for case-insensitive matching
    query_lower = query.lower()

    # Define state and crop patterns
    state_pattern = r"(maharashtra|punjab|karnataka|kerala|tamil\s+nadu|gujarat|andhra\s+pradesh|telangana|uttar\s+pradesh|madhya\s+pradesh|rajasthan|haryana|west\s+bengal|bihar|odisha|assam)"
    crop_pattern = r"(rice|wheat|cotton|sugarcane|maize|soybean|pulses|groundnut|sunflower|barley|jowar|bajra|linseed|mustard|coconut|tea|coffee|spices)"
    years_pattern = r"(\d+)\s*year"

    # Extract entities (case-insensitive for states and crops)
    states_raw = re.findall(state_pattern, query_lower)
    crops_raw = re.findall(crop_pattern, query_lower)
    years = re.findall(years_pattern, query_lower)

    # Normalize state names (capitalize properly)
    state_mapping = {
        "maharashtra": "Maharashtra",
        "punjab": "Punjab",
        "karnataka": "Karnataka",
        "kerala": "Kerala",
        "tamil nadu": "Tamil Nadu",
        "gujarat": "Gujarat",
        "andhra pradesh": "Andhra Pradesh",
        "telangana": "Telangana",
        "uttar pradesh": "Uttar Pradesh",
        "madhya pradesh": "Madhya Pradesh",
        "rajasthan": "Rajasthan",
        "haryana": "Haryana",
        "west bengal": "West Bengal",
        "bihar": "Bihar",
        "odisha": "Odisha",
        "assam": "Assam"
    }

    states = [state_mapping[s] for s in states_raw if s in state_mapping]

    # Normalize crop names (capitalize)
    crops = [c.capitalize() for c in crops_raw]

    # Determine analysis type based on query keywords
    analysis_type = "general"
    if any(word in query_lower for word in ["correlation", "relationship", "impact", "effect", "influence"]):
        analysis_type = "correlation"
    elif any(word in query_lower for word in ["trend", "growth", "decline", "change"]):
        analysis_type = "trend"
    elif any(word in query_lower for word in ["top", "highest", "best", "maximum", "rank"]):
        analysis_type = "ranking"
    elif any(word in query_lower for word in ["compare", "comparison", "vs", "versus"]):
        analysis_type = "comparison"
    elif any(word in query_lower for word in ["rainfall", "rain", "precipitation", "weather", "climate"]):
        analysis_type = "climate"

    return {
        "states": states,
        "crops": crops,
        "years": int(years[0]) if years else 5,
        "analysis_type": analysis_type
    }
