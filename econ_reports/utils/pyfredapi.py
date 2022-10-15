"""Utility functions for pyfredapi. If I like something enough I may move it into pyfredapi.
"""

from typing import List

from pyfredapi import FredSeries
from rich.console import Console

console = Console()


class SeriesCollection:
    """A collection of pyfredapi.SeriesData objects."""

    def __init__(self, client: FredSeries, series: List[str]):
        self.client = client
        self.series = series

        responses = {}
        for s in series:
            print(f"Requesting series {s}...")
            response = client.get_series(series_id=s)
            responses[s] = response

        for series_name, series_data in responses.items():
            setattr(self, series_name, series_data)

        self.responses = self.__dict__.copy()
        _ = self.responses.pop("client", None)
        _ = self.responses.pop("series", None)

    def show_seasonality(self) -> None:
        """"""
        seasonal_adjustments = [
            series_data.info.seasonal_adjustment
            for series_data in list(self.responses.values())
        ]
        distinct_seasonality = set(seasonal_adjustments)

        if len(distinct_seasonality) == 1:
            print(f"All series are {distinct_seasonality.pop()}")
            return

        for season in distinct_seasonality:
            console.rule(f"[bold red]Series that are {season}")
            for series_data in list(self.responses.values()):
                if series_data.info.seasonal_adjustment == season:
                    console.print(f"{series_data.info.id}: {series_data.info.title}")

    def show_frequency(self) -> None:
        """"""
        frequencies = [
            series_data.info.frequency for series_data in list(self.responses.values())
        ]
        distinct_freq = set(frequencies)

        if len(distinct_freq) == 1:
            print(f"All series are {distinct_freq.pop()}")
            return

        for freq in distinct_freq:
            console.rule(f"[bold red]Series that are published {freq}")
            for series_data in list(self.responses.values()):
                if series_data.info.frequency == freq:
                    console.print(f"{series_data.info.id}: {series_data.info.title}")

    def show_observation_end(self) -> None:
        """"""
        end_dates = [
            series_data.info.observation_end
            for series_data in list(self.responses.values())
        ]
        distinct_end_dates = set(end_dates)

        if len(distinct_end_dates) == 1:
            print(f"All series end on {distinct_end_dates.pop()}")
            return

        for date in distinct_end_dates:
            console.rule(f"[bold red]Series that end on {date}")
            for series_data in list(self.responses.values()):
                if series_data.info.observation_end == date:
                    console.print(f"{series_data.info.id}: {series_data.info.title}")

    def extract_series(self):
        """Return a new instance of SeriesCollection, with a subset of data from this instance."""
        raise NotImplementedError


def get_series(client: FredSeries, series: List[str]) -> SeriesCollection:
    """Take a list of FRED series and returns a SeriesCollection."""

    responses = {}
    for s in series:
        print(f"Requesting series {s}...")
        response = client.get_series(series_id=s)
        responses[s] = response

    return SeriesCollection(**responses)
