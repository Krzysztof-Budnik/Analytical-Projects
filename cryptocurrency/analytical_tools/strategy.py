from data import IndicatorData
from errors import ParameterNotFoundError


class Strategy():
    """Strategy class determines how trades are going to be executed."""
        
    def __init__(self, indicator_data: IndicatorData, parameters: dict[str: bool]) -> None:
        """indicatodr_data is supposed to contain evaluation colums (formated as boolean expressions), 
        parameters dict contains bolean column names as keys and desired bolean state as values."""
        
        self.indicator_data = indicator_data
        self.parameters = parameters
        self.parameter_names = list(self.parameters.keys())
        self.parameter_values = list(self.parameters.values())
        self.symbols = self.indicator_data.symbols
        self.dataframes = self.indicator_data.dataframes
       
    def __repr__(self) -> str:
        return f'Strategy \nDesired parameter states: {self.parameters}'
    
    def __getitem__(self, key) -> bool:
        return self.parameters[key]
    
    def define_position_status(self, add_lag_column=False) -> IndicatorData:
        """Method adds in_position variable to dataframes. When all conditions 
        described in parameters are true then in_position"""
        
        for param in self.parameter_names:
            if self.indicator_data.columns().count(param) != 1:
                raise ParameterNotFoundError(param)
            
        num_param = len(self.parameter_names)   
        for df in self.dataframes:
            df['in_position'] = all(self.parameter_values)
            df.drop(df.iloc[:, 1:-num_param], axis = 1, inplace = True)

            if add_lag_column:
                df['in_position_lag'] = df['in_position'].shift(1)
                df.drop([df.index[0]], inplace=True)
                
        return self.indicator_data
    