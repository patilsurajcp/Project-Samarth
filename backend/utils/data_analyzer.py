import pandas as pd

def calculate_correlation(df_rain, df_crop):
    """
    Calculate correlation between rainfall and crop production.

    Args:
        df_rain: DataFrame with rainfall data
        df_crop: DataFrame with crop production data

    Returns:
        Dictionary with correlation analysis
    """
    try:
        # Merge rainfall and crop data by state
        merged = pd.merge(
            df_rain.groupby("State")["Rainfall"].mean().reset_index(),
            df_crop.groupby("State")["Production"].sum().reset_index(),
            on="State"
        )

        if len(merged) < 2:
            return {"correlation": None, "interpretation": "Insufficient data for correlation"}

        correlation = merged["Rainfall"].corr(merged["Production"])

        # Interpret correlation
        if correlation > 0.7:
            interpretation = "Strong positive correlation - Higher rainfall strongly associated with higher production"
        elif correlation > 0.3:
            interpretation = "Moderate positive correlation - Higher rainfall generally associated with higher production"
        elif correlation > -0.3:
            interpretation = "Weak or no correlation - Rainfall has minimal impact on production"
        elif correlation > -0.7:
            interpretation = "Moderate negative correlation - Higher rainfall associated with lower production"
        else:
            interpretation = "Strong negative correlation - Higher rainfall strongly associated with lower production"

        return {
            "correlation": round(correlation, 3),
            "interpretation": interpretation,
            "data_points": len(merged)
        }
    except Exception as e:
        return {"correlation": None, "error": str(e)}

def perform_analysis(datasets, entities):
    """
    Analyze rainfall and crop production data with advanced analytics.

    Args:
        datasets: Dictionary containing 'rainfall' and 'crop' data
        entities: Dictionary containing 'states', 'crops', 'years', 'analysis_type'

    Returns:
        Dictionary with comprehensive analysis results
    """
    try:
        df_rain = pd.DataFrame(datasets["rainfall"])
        df_crop = pd.DataFrame(datasets["crop"])

        # Normalize column names (handle both uppercase and lowercase)
        df_rain.columns = [col.capitalize() for col in df_rain.columns]
        df_crop.columns = [col.capitalize() for col in df_crop.columns]

        # Validate required columns exist
        if "State" not in df_rain.columns or "Rainfall" not in df_rain.columns:
            raise ValueError("Rainfall data must contain 'State' and 'Rainfall' columns")
        if "State" not in df_crop.columns or "Production" not in df_crop.columns:
            raise ValueError("Crop data must contain 'State' and 'Production' columns")

        # Filter by states if provided in entities
        if entities.get("states"):
            df_rain = df_rain[df_rain["State"].isin(entities["states"])]
            df_crop = df_crop[df_crop["State"].isin(entities["states"])]

        # Perform analysis based on type
        analysis_type = entities.get("analysis_type", "general")

        # Rainfall analysis
        rainfall_result = df_rain.groupby("State")["Rainfall"].agg(["mean", "min", "max"]).reset_index()
        rainfall_result.columns = ["State", "Average_Rainfall", "Min_Rainfall", "Max_Rainfall"]

        # Crop analysis
        if "Crop" in df_crop.columns:
            # Top crops per state
            crops = df_crop.groupby(["State", "Crop"])["Production"].sum().reset_index()
            crops = crops.sort_values(["State", "Production"], ascending=[True, False])
            crops = crops.groupby("State").head(10).reset_index(drop=True)
        else:
            # Total production by state
            crops = df_crop.groupby("State")["Production"].sum().reset_index()
            crops.columns = ["State", "Total_Production"]

        # Correlation analysis
        correlation_analysis = calculate_correlation(df_rain, df_crop)

        # State-wise comparison
        state_comparison = pd.merge(
            rainfall_result,
            df_crop.groupby("State")["Production"].sum().reset_index(),
            on="State",
            how="left"
        )

        result = {
            "rainfall_analysis": rainfall_result.to_dict(orient="records"),
            "crop_analysis": crops.to_dict(orient="records"),
            "correlation_analysis": correlation_analysis,
            "state_comparison": state_comparison.to_dict(orient="records"),
            "analysis_type": analysis_type
        }

        return result
    except KeyError as e:
        raise KeyError(f"Missing required key in datasets: {e}")
    except Exception as e:
        raise Exception(f"Error during data analysis: {e}")
