# QUESTION 1.
import pandas as pd

def generate_car_matrix(input_df):
    car_matrix = input_df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[i for i in range(len(car_matrix))], [i for i in range(len(car_matrix))]] = 0
    car_matrix = car_matrix.transpose()
    return car_matrix
file_path = 'C:/Users/launc/Downloads/dataset-1.csv'
df = pd.read_csv(file_path)
generated_matrix = generate_car_matrix(df)
print(generated_matrix.iloc[:5, :5])


#Question 2:
import pandas as pd

def get_type_count(input_df):
    input_df['car_type'] = pd.cut(input_df['car'],
                                  bins=[float('-inf'), 15, 25, float('inf')],
                                  labels=['low', 'medium', 'high'],
                                  right=False)
    
    type_count = input_df['car_type'].value_counts().to_dict()
    type_count = dict(sorted(type_count.items()))
    
    return type_count
file_path = 'C:/Users/launc/Downloads/dataset-1.csv'
df = pd.read_csv(file_path)
result = get_type_count(df)
print(result)

#Question 3:
import pandas as pd

def get_bus_indexes(input_df):
    mean_bus_value = input_df['bus'].mean()
    bus_indexes = input_df[input_df['bus'] > 2 * mean_bus_value].index.tolist()
    bus_indexes.sort()

    return bus_indexes

file_path = 'C:/Users/launc/Downloads/dataset-1.csv'
df = pd.read_csv(file_path)
bus_indices = get_bus_indexes(df)

print(f"The indices where bus values are greater than twice the mean: {bus_indices}")

#Question 4:

import pandas as pd

def filter_routes(input_df):
    average_truck_by_route = input_df.groupby('route')['truck'].mean()
    selected_routes = average_truck_by_route[average_truck_by_route > 7].index.tolist()
    selected_routes.sort()

    return selected_routes
file_path = 'C:/Users/launc/Downloads/dataset-1.csv'
df = pd.read_csv(file_path)
selected_routes = filter_routes(df)

print(f"The sorted list of routes with average truck values greater than 7: {selected_routes}")

#question 5:

import pandas as pd

def multiply_matrix(input_matrix):
    modified_matrix = input_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)

    return modified_matrix
modified_matrix = multiply_matrix(generated_matrix)

print("Original Matrix:")
print(generated_matrix.iloc[:5, :5])
print("\nModified Matrix:")
print(modified_matrix.iloc[:5, :5])

#Question 6:

import pandas as pd

def check_time_completeness(input_df):
    input_df['start_timestamp'] = pd.to_datetime(input_df['startDay'] + ' ' + input_df['startTime'], format='%A %H:%M:%S')
    input_df['end_timestamp'] = pd.to_datetime(input_df['endDay'] + ' ' + input_df['endTime'], format='%A %H:%M:%S')
    input_df['start_day'] = input_df['start_timestamp'].dt.day_name()
    input_df['start_time'] = input_df['start_timestamp'].dt.time
    input_df['end_day'] = input_df['end_timestamp'].dt.day_name()
    input_df['end_time'] = input_df['end_timestamp'].dt.time
    completeness_check = input_df.groupby(['id', 'id_2']).apply(
        lambda group: (
            (group['start_day'].nunique() == 7) and
            (group['start_time'].min() == pd.Timestamp('1900-01-01 00:00:00').time()) and
            (group['end_time'].max() == pd.Timestamp('1900-01-01 23:59:59').time())
        )
    )

    return completeness_check

file_path = 'C:/Users/launc/Downloads/dataset-2.csv'
df = pd.read_csv(file_path)
completeness_result = check_time_completeness(df)

print("Completeness Check for each (id, id_2) pair:")
print(completeness_result)