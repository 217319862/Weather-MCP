from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("weather")


@mcp.tool()
def get_weather(city: str) -> str:
    """מחזיר מזג אוויר נוכחי לפי שם עיר (למשל Tel Aviv)"""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10,
        )
        geo.raise_for_status()
        results = geo.json().get("results")
        if not results:
            return f"לא נמצאה עיר בשם {city}"

        place = results[0]
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current_weather": True,
            },
            timeout=10,
        )
        resp.raise_for_status()
        w = resp.json()["current_weather"]

        return (f"[MCP] {place['name']}: טמפרטורה {w['temperature']}°C, "
                f"רוח {w['windspeed']} קמ״ש")
    except Exception as e:
        return f"שגיאה ב-get_weather: {type(e).__name__}: {e}"


if __name__ == "__main__":
    mcp.run()