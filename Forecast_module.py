import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from matplotlib.figure import Figure


def haal_weersdata_op(latitude=52.0908, longitude=5.1222):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "precipitation_sum"],
        "timezone": "auto"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    daily = response.Daily()

    data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),
        "precipitation_sum": daily.Variables(1).ValuesAsNumpy()
    }

    return pd.DataFrame(data)




def maak_forecast_figuur(df):
    fig = Figure(figsize=(4/(2/3), 4))
    ax1 = fig.add_subplot(111)

    fig.patch.set_facecolor("white")
    ax1.set_facecolor("#f1f1ff")

    ax1.plot(
        df["date"],
        df["temperature_2m_max"],
        color="#7777cc",
        marker="o"
    )
    ax1.set_ylabel("Temperatuur (°C)", color="#7777cc")

    ax2 = ax1.twinx()
    ax2.bar(
        df["date"],
        df["precipitation_sum"],
        alpha=0.3,
        color="#9999ee"
    )
    ax2.set_ylabel("Neerslag (mm)", color="#9999ee")

    ax1.set_title("Weersverwachting")
    fig.autofmt_xdate()
    ax1.grid(True, alpha=0.3)

    return fig

def Forecast_module():
    df = haal_weersdata_op()
    return maak_forecast_figuur(df)


if __name__ == "__main__":
    Forecast_module()