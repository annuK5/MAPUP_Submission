# Question 1:

import pandas as pd

def calculate_distance_matrix(input_df):
    distance_matrix = input_df.pivot_table(values='distance', index='id_start', columns='id_end', fill_value=0)
    distance_matrix = distance_matrix.add(distance_matrix.T, fill_value=0)
    distance_matrix.values[[range(len(distance_matrix))]*2] = 0
    for intermediate_point in distance_matrix.columns:
        for start_point in distance_matrix.index:
            for end_point in distance_matrix.index:

                if distance_matrix.at[start_point, end_point] == 0 and start_point != end_point:
                    distance_start_to_intermediate = distance_matrix.at[start_point, intermediate_point]
                    distance_intermediate_to_end = distance_matrix.at[intermediate_point, end_point]
                    
                    if distance_start_to_intermediate > 0 and distance_intermediate_to_end > 0:
                        cumulative_distance = distance_start_to_intermediate + distance_intermediate_to_end
                        if distance_matrix.at[start_point, end_point] == 0 or cumulative_distance < distance_matrix.at[start_point, end_point]:
                            distance_matrix.at[start_point, end_point] = cumulative_distance
    
    return distance_matrix

file_path = 'C:/Users/launc/Downloads/dataset-3.csv'
df = pd.read_csv(file_path)
completeness_result = calculate_distance_matrix(df)

print("Sample result dataframe:")
print(completeness_result.iloc[:7, :7])

#Question 2:
import pandas as pd

def unroll_distance_matrix(distance_matrix):
    unrolled_data = []

    for start_point in distance_matrix.index:
        for end_point in distance_matrix.columns:
            if start_point != end_point:
                distance = distance_matrix.at[start_point, end_point]

                unrolled_data.append({'id_start': start_point, 'id_end': end_point, 'distance': distance})

    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df
file_path = 'C:/Users/launc/Downloads/dataset-3.csv'
df = pd.read_csv(file_path)
unrolled_distance_df = unroll_distance_matrix(df)

print("Unrolled Distance DataFrame:")
print(unrolled_distance_df)

#Question 3:
import pandas as pd

def find_ids_within_ten_percentage_threshold(df, reference_value):
    reference_df = df[df['id_start'] == reference_value]
    average_distance = reference_df['distance'].mean()
    threshold = 0.1 * average_distance

    filtered_ids = df[(df['distance'] >= (average_distance - threshold)) & (df['distance'] <= (average_distance + threshold))]

    result_ids = sorted(filtered_ids['id_start'].unique())

    return result_ids

reference_value = 1001400  
result_ids = find_ids_within_ten_percentage_threshold(unrolled_distance_df, reference_value)

print(f"IDs within 10% threshold of average distance for ID {reference_value}:")
print(result_ids)

#Question 4:

import pandas as pd

def calculate_toll_rate(input_df):
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    toll_rate_df = pd.DataFrame(columns=['id_start', 'id_end', 'moto', 'car', 'rv', 'bus', 'truck'])

    toll_rate_df['id_start'] = input_df['id_start']
    toll_rate_df['id_end'] = input_df['id_end']

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        toll_rate_df[vehicle_type] = input_df['distance'] * rate_coefficient

    return toll_rate_df



file_path = 'C:/Users/launc/Downloads/dataset-3.csv'
df = pd.read_csv(file_path)
completeness_result = calculate_toll_rate(df)

print("Sample result dataframe:")
print(completeness_result.iloc[:7, :7])

#Question 5:
import pandas as pd
from datetime import time

def calculate_time_based_toll_rates(input_df):
    time_ranges_weekdays = [(time(0, 0), time(10, 0)), (time(10, 0), time(18, 0)), (time(18, 0), time(23, 59, 59))]
    time_ranges_weekends = [(time(0, 0), time(23, 59, 59))]
    
    discount_factors_weekdays = [0.8, 1.2, 0.8]
    discount_factor_weekends = 0.7

    frames = []

    for _, row in input_df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']

        for day in range(7): 
            for time_range, discount_factor in zip(time_ranges_weekdays, discount_factors_weekdays):
                start_time, end_time = time_range
                frames.append(pd.DataFrame({
                    'id_start': [id_start],
                    'id_end': [id_end],
                    'start_day': [day],
                    'start_time': [start_time],
                    'end_day': [day],
                    'end_time': [end_time],
                    'motor': [row['moto'] * discount_factor],
                    'car': [row['car'] * discount_factor],
                    'rv': [row['rv'] * discount_factor],
                    'bus': [row['bus'] * discount_factor],
                    'truck': [row['truck'] * discount_factor]
                }))

            for time_range in time_ranges_weekends:
                start_time, end_time = time_range
                frames.append(pd.DataFrame({
                    'id_start': [id_start],
                    'id_end': [id_end],
                    'start_day': [day],
                    'start_time': [start_time],
                    'end_day': [day],
                    'end_time': [end_time],
                    'motor': [row['moto'] * discount_factor_weekends],
                    'car': [row['car'] * discount_factor_weekends],
                    'rv': [row['rv'] * discount_factor_weekends],
                    'bus': [row['bus'] * discount_factor_weekends],
                    'truck': [row['truck'] * discount_factor_weekends]
                }))

    time_based_toll_df = pd.concat(frames, ignore_index=True)

    time_based_toll_df['start_time'] = pd.to_datetime(time_based_toll_df['start_time'], format='%H:%M:%S').dt.time
    time_based_toll_df['end_time'] = pd.to_datetime(time_based_toll_df['end_time'], format='%H:%M:%S').dt.time

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    time_based_toll_df['start_day'] = time_based_toll_df['start_day'].map({i: day for i, day in enumerate(days_of_week)})
    time_based_toll_df['end_day'] = time_based_toll_df['end_day'].map({i: day for i, day in enumerate(days_of_week)})

    return time_based_toll_df

result_df_with_time_based_toll_rates = calculate_time_based_toll_rates(unrolled_distance_df)

print("DataFrame with Time-Based Toll Rates:")
print(result_df_with_time_based_toll_rates.head())
