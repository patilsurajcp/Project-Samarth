import requests
import logging

logger = logging.getLogger(__name__)

# Data.gov.in API endpoints
RAINFALL_API = "https://data.gov.in/node/135611/datastore/export/json"
CROP_PRODUCTION_API = "https://data.gov.in/node/135612/datastore/export/json"

def fetch_live_data(api_url, timeout=5):
    """
    Fetch data from live data.gov.in API.

    Args:
        api_url: The API endpoint URL
        timeout: Request timeout in seconds

    Returns:
        List of records or empty list if request fails
    """
    try:
        response = requests.get(api_url, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        # Handle different response formats
        if isinstance(data, dict):
            if "records" in data:
                return data["records"]
            elif "data" in data:
                return data["data"]
        elif isinstance(data, list):
            return data

        return []
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to fetch from {api_url}: {e}")
        return []

def fetch_data(entities):
    """
    Fetch rainfall and crop production data from live and mock sources.

    Args:
        entities: Dictionary containing 'states', 'crops', 'years'

    Returns:
        Dictionary with rainfall, crop data, and sources
    """
    # Use provided states or default to all major states
    states = entities.get("states") or ["Maharashtra", "Punjab", "Karnataka", "Kerala", "Tamil Nadu", "Gujarat"]

    # Available crops
    crops_list = ["Rice", "Wheat", "Cotton", "Sugarcane", "Maize", "Soybean", "Pulses", "Groundnut", "Sunflower", "Barley"]

    # Try to fetch live data first
    live_rainfall = fetch_live_data(RAINFALL_API)
    live_crops = fetch_live_data(CROP_PRODUCTION_API)

    # If live data is available, use it; otherwise use mock data
    if live_rainfall:
        rainfall_data = live_rainfall
    else:
        # Mock rainfall data
        rainfall_data = [{"State": s, "Year": y, "Rainfall": 1000 + idx * 50}
                         for idx, s in enumerate(states)
                         for y in range(2018, 2023)]

    if live_crops:
        crop_data = live_crops
    else:
        # Mock crop data with multiple crops per state
        crop_data = []
        for idx, s in enumerate(states):
            for crop_idx, crop in enumerate(crops_list):
                production = 5000 + idx * 200 + crop_idx * 150
                crop_data.append({
                    "State": s,
                    "Crop": crop,
                    "Production": production
                })

    # Filter data by selected states if available
    if states:
        rainfall_data = [r for r in rainfall_data if r.get("State") in states or r.get("state") in states]
        crop_data = [c for c in crop_data if c.get("State") in states or c.get("state") in states]

    return {
        "rainfall": rainfall_data,
        "crop": crop_data,
        "sources": [
            "https://data.gov.in/catalog/rainfall-india",
            "https://data.gov.in/catalog/state-wise-season-wise-crop-production-statistics"
        ],
        "data_source": "live" if live_rainfall or live_crops else "mock"
    }
