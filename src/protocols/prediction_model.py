from typing import Protocol

import numpy as np
import pandas as pd


class PredictionModelProtocol(Protocol):
    def predict(self, X: pd.DataFrame) -> np.ndarray: ...
