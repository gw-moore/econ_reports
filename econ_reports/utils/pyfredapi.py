"""Utility functions for pyfredapi. If I like something enough I may move it into pyfredapi.
"""

from typing import List, Union

from pyfredapi import FredSeries
from rich.console import Console

console = Console()


class SeriesCollection:
    """A collection of pyfredapi.SeriesData objects.

    Parameters
    ----------
    client : FredSeries
        A FredSeries object.
    """

    def __init__(self, client: FredSeries = FredSeries()):
        self.client = client
        self.responses = {}
        self._source = {}

    def add_series(
        self,
        series: Union[str, List[str]],
        drop_realtime: bool = True,
        set_col_name_to_series_id: bool = True,
    ) -> None:
        """Add series to class instance.

        Parameters
        ----------
        series : Union[str, List[str]]
            Series to add to collection.
        drop_realtime : bool
            Indicates if you want to drop the realtime columns.
        set_col_name_to_series_id : bool
            Indicates if you want to rename the value column to series id.
        """
        if isinstance(series, str):
            series = [series]

        for series_name in series:
            if series_name in self.responses:
                print(f"Already have {series_name}")
            else:
                print(f"Requesting series {series_name}...")
                response = self.client.get_series(series_id=series_name)
                if drop_realtime:
                    response.data.drop(
                        ["realtime_start", "realtime_end"], inplace=True, axis=1
                    )
                if set_col_name_to_series_id:
                    response.data.rename(columns={"value": series_name}, inplace=True)
                self.responses[series_name] = response
                setattr(self, series_name, response)

    def drop_series(self, series: Union[str, List[str]]) -> None:
        """Drop series from collection.

        Parameters
        ----------
        series : Union[str, List[str]]
            Series to remove from collection.
        """
        if isinstance(series, str):
            series = [series]

        for series_name in series:
            try:
                del self.responses[series_name]
            except KeyError:
                print(f"No series {series_name} in collection")
            delattr(self, series_name)
            print(f"Removed series {series_name}")

    def list_series(self):
        """List the series in the collection."""
        for series_data in list(self.responses.values()):
            console.print(f"{series_data.info.id}: {series_data.info.title}")

    def show_seasonality(self) -> None:
        """Show seasonality of the series."""
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
        """Show frequency of the series."""
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
        """Show the latest date of the series."""
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
