class ParameterNotFoundError(Exception):
    def __init__(self, parameter: str) -> None:
        self.parameter = parameter
        self.message = \
        f"""Could not find '{self.parameter}' parameter in the instance of IndicatorData.
Possible reasons: 
1) spelling mistake (one of the keys) in parameters dictionary
2) IndicatorData does not contain parameter column and thus is incorrectly formatted"""

        super().__init__(self.message)