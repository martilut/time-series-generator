from math import sqrt

from numpy import array
from numpy.random import normal, randint, uniform

from src.main.process import Process
from src.main.time_series import TimeSeries
from src.main.utils.utils import draw_process_plot


class WhiteNoiseProcess(Process):
    def __init__(self):
        self.distributions = {0: normal, 1: uniform}

    @property
    def name(self) -> str:
        return "white_noise"

    @property
    def lag(self) -> int:
        return 0

    @property
    def num_parameters(self) -> int:
        return 3

    def generate_parameters(
        self, low_value: float, high_value: float
    ) -> tuple[float, float, float]:
        distribution_id = randint(0, len(self.distributions.keys()))
        if distribution_id == 0:
            mean = uniform(low_value, high_value)
            std = uniform(low_value, high_value)
            return distribution_id, mean, sqrt(abs(std))
        else:
            low = uniform(low_value, high_value)
            high = uniform(low_value, high_value)
            return distribution_id, min(low, high), max(low, high)

    def generate_init_values(self, low_value: float, high_value: float) -> array:
        return array([])

    def get_info(
        self, sample: tuple[int, tuple], init_values: tuple[float, ...] = None
    ) -> dict:
        info = dict()
        info["name"] = self.name
        info["lag"] = self.lag
        info["distribution"] = self.distributions[sample[1][0]].__name__
        info["parameters"] = ["{:.3f}".format(i) for i in sample[1][1:]]
        info["initial_values"] = None
        return info

    def generate_time_series(
        self,
        sample: tuple[int, tuple],
        previous_values: array = None,
        border_values: tuple[float, float] = None,
    ) -> tuple[TimeSeries, dict]:
        distribution_id, *parameters = sample[1]
        wn_values = self.distributions[distribution_id](size=sample[0], *parameters)
        wn_time_series = TimeSeries()
        wn_time_series.add_values(wn_values, (self.name, sample))
        return wn_time_series, self.get_info(sample)

    def draw_plot(
        self,
        border_values: tuple[float, float] = None,
        path: str = None,
        time_series_data: tuple[TimeSeries, dict] = None,
    ) -> None:
        if time_series_data is None:
            sample = self.generate_parameters(border_values[0], border_values[1])
            data = self.generate_time_series((100, sample))
        else:
            data = time_series_data
        if path is not None:
            draw_process_plot(
                data[0].get_values(), data[1], path=f"{path}\\{self.name}_plot.png"
            )
        else:
            draw_process_plot(data[0].get_values(), data[1])
        return
