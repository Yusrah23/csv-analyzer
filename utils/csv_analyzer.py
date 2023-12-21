import pandas as pd
import matplotlib.pyplot as plt

class CsvAnalyzer:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.is_accessible = self.is_usable()

    def is_usable(self):
        pass

    def summary(self):
        summarization = {

        }
        return summarization

    def clean(self, dropna=True):
        if dropna:
            self.data = self.data.dropna()

    def analyze(self):
        analysis_result = {}

        for col in self.data.columns:
            if col in self.data.select_dtypes(include=['number']).columns:
                analysis_result[f'{col}_mean'] = self.data[col].mean()
                analysis_result[f'{col}_median'] = self.data[col].median()
                analysis_result[f'{col}_std'] = self.data[col].std()

            elif col in self.data.select_dtypes(include=['object']).columns:
                analysis_result[f'{col}_value_counts'] = self.data[col].value_counts()
                analysis_result[f'{col}_unique'] = self.data[col].unique()

        return analysis_result

    def visualize(self, column_name):
        pass

    def identify_special_columns(self):
        remove_keywords = ['price', 'sale', 'amount', quantity]
        add_keywords = ['code', 'type', 'category', 'class', 'status', 'flag', 'mode', 'method', 'version']
        
        special_columns_to_remove = [col for col in self.data.columns if any(keyword in col.lower() for keyword in remove_keywords)]
        special_columns_to_add = [col for col in self.data.columns if any(keyword in col.lower() for keyword in add_keywords)]
        
        return special_columns_to_remove, special_columns_to_add

    def detect_categorical_columns(self, threshold=0.05):
        categorical_columns = self.data.select_dtypes(include=['object']).columns.tolist()

        special_columns_to_remove, special_columns_to_add = self.identify_special_columns()
        categorical_columns = [col for col in categorical_columns if col not in special_columns_to_remove]
        categorical_columns += special_columns_to_add

        numerical_columns = self.data.select_dtypes(include=['number']).columns.tolist()
        potential_categorical_columns = [col for col in numerical_columns if
                                         self.data[col].nunique() / len(self.data[col]) <= threshold]

        categorical_columns += potential_categorical_columns

        return categorical_columns

    def detect_datetime_columns(self):
        datetime_columns = self.data.select_dtypes(include=['datetime']).columns.tolist()

        for col in self.data.columns:
            try:
                if pd.to_datetime(self.data[col], errors='raise').dtype == 'datetime64[ns]':
                    datetime_columns.append(col)
            except (ValueError, TypeError):
                pass

        return datetime_columns
