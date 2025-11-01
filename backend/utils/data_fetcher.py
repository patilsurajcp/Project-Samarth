import os
import requests
import logging

logger = logging.getLogger(__name__)

# Data.gov.in API endpoints (fallback export endpoints if API key/resources are not provided)
RAINFALL_EXPORT_API = "https://data.gov.in/node/135611/datastore/export/json"
CROP_PRODUCTION_EXPORT_API = "https://data.gov.in/node/135612/datastore/export/json"

# CKAN Datastore API base
CKAN_DATASTORE_URL = "https://data.gov.in/api/datastore/resource.json"

DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY", "").strip()
RAINFALL_RESOURCE_ID = os.getenv("RAIN_FALL_RESOURCE_ID", os.getenv("RAINFALL_RESOURCE_ID", "").strip())
CROP_PRODUCTION_RESOURCE_ID = os.getenv("CROP_PROD_RESOURCE_ID", os.getenv("CROP_PRODUCTION_RESOURCE_ID", "").strip())

def fetch_ckan_resource(resource_id: str, limit: int = 1000, offset: int = 0, filters: dict | None = None, timeout: int = 10):
    """
    Fetch records from data.gov.in CKAN datastore for a given resource.

    Requires env DATA_GOV_API_KEY to be set. Supports simple pagination via limit/offset.
    """
    if not DATA_GOV_API_KEY or not resource_id:
        return []

    try:
        params = {
            "api-key": DATA_GOV_API_KEY,
            "resource_id": resource_id,
            "limit": limit,
            "offset": offset,
        }
        if filters:
            # CKAN expects JSON-encoded filters; requests will encode dict appropriately
            params["filters"] = filters

        response = requests.get(CKAN_DATASTORE_URL, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            # Standard CKAN returns { result: { records: [...] } }
            result = data.get("result") or {}
            records = result.get("records")
            if isinstance(records, list):
                return records
            # Some endpoints may directly return records
            if "records" in data and isinstance(data["records"], list):
                return data["records"]
        return []
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed CKAN fetch for resource {resource_id}: {e}")
        return []

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

    # Try to fetch via CKAN API first (if API key and resource IDs provided)
    live_rainfall = []
    live_crops = []

    if DATA_GOV_API_KEY and (RAINFALL_RESOURCE_ID or CROP_PRODUCTION_RESOURCE_ID):
        try:
            # Basic pagination attempt to gather up to ~3000 rows per resource
            if RAINFALL_RESOURCE_ID:
                chunk = []
                offset = 0
                while True:
                    records = fetch_ckan_resource(RAINFALL_RESOURCE_ID, limit=1000, offset=offset)
                    if not records:
                        break
                    chunk.extend(records)
                    if len(records) < 1000:
                        break
                    offset += 1000
                live_rainfall = chunk

            if CROP_PRODUCTION_RESOURCE_ID:
                chunk = []
                offset = 0
                while True:
                    records = fetch_ckan_resource(CROP_PRODUCTION_RESOURCE_ID, limit=1000, offset=offset)
                    if not records:
                        break
                    chunk.extend(records)
                    if len(records) < 1000:
                        break
                    offset += 1000
                live_crops = chunk
        except Exception as e:
            logger.warning(f"CKAN fetch error: {e}")

    # Fallback to public export endpoints if CKAN not configured or empty
    if not live_rainfall:
        live_rainfall = fetch_live_data(RAINFALL_EXPORT_API)
    if not live_crops:
        live_crops = fetch_live_data(CROP_PRODUCTION_EXPORT_API)

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
        "data_source": "live" if (live_rainfall or live_crops) else "mock"
    }
