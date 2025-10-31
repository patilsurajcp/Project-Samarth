def generate_summary(analysis_result, query):
    """
    Generate a comprehensive summary of the analysis results.

    Args:
        analysis_result: Dictionary with analysis results
        query: Original user query

    Returns:
        Formatted summary string
    """
    try:
        rainfall_data = analysis_result.get("rainfall_analysis", [])
        crop_data = analysis_result.get("crop_analysis", [])
        correlation = analysis_result.get("correlation_analysis", {})
        analysis_type = analysis_result.get("analysis_type", "general")

        if not rainfall_data:
            return "No data available for the specified query."

        # Extract states
        states = [r.get("State") for r in rainfall_data if "State" in r]
        states_str = ", ".join(states) if states else "selected regions"

        # Build summary based on analysis type
        summary_parts = []

        if analysis_type == "correlation":
            correlation_value = correlation.get("correlation")
            interpretation = correlation.get("interpretation", "")
            if correlation_value is not None:
                summary_parts.append(f"Correlation Analysis: {interpretation} (Correlation coefficient: {correlation_value})")
            else:
                summary_parts.append("Correlation analysis could not be performed with available data.")

        elif analysis_type == "ranking":
            if crop_data:
                top_crop = crop_data[0] if isinstance(crop_data, list) else {}
                summary_parts.append(f"Top performing crop: {top_crop.get('Crop', 'N/A')} with production of {top_crop.get('Production', 'N/A')} units")

        elif analysis_type == "climate":
            if rainfall_data:
                avg_rainfall = sum(r.get("Average_Rainfall", 0) for r in rainfall_data) / len(rainfall_data)
                summary_parts.append(f"Average rainfall across {states_str}: {avg_rainfall:.0f}mm")

        elif analysis_type == "trend":
            summary_parts.append(f"Analyzing trends for {states_str}")

        elif analysis_type == "comparison":
            summary_parts.append(f"Comparing agricultural metrics across {states_str}")

        else:  # general
            summary_parts.append(f"Agricultural analysis for {states_str}")
            if rainfall_data:
                avg_rainfall = sum(r.get("Average_Rainfall", 0) for r in rainfall_data) / len(rainfall_data)
                summary_parts.append(f"Average rainfall: {avg_rainfall:.0f}mm")
            if crop_data:
                total_production = sum(c.get("Production", 0) for c in crop_data)
                summary_parts.append(f"Total crop production: {total_production} units")
            if correlation.get("correlation") is not None:
                summary_parts.append(f"Rainfall-Production Correlation: {correlation.get('interpretation', '')}")

        summary = ". ".join(summary_parts) + f". Query: {query}"
        return summary

    except Exception as e:
        return f"Error generating summary: {str(e)}"
