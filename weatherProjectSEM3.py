# 1. Importing Libraries and Data Preparation (Wasam Jaffri)
import tkinter as tk  # GUI banane ke liye
from tkinter import messagebox, filedialog  # pop-up messages aur file browse karne ke liye
import matplotlib.pyplot as plt  # Graphs banane ke liye
from sklearn.linear_model import LinearRegression  # Linear regression model
import pandas as pd  # Tabular data handle karne ke liye
import random  # Random values generate karne ke liye

# Sample weather data
weather_data = {
    'temperature': [30, 25, 35, 40, 28, 22, 32, 45, 0, 30, 24, 32, 11, 23, 17, 19, 21,
                    -45, -38, -27, -32, -14, -50, -43, -22, -18, -36, -11, -29, -33, -17, -44, -40, -31, -24, -19, -28],
    'humidity': [70, 65, 80, 90, 60, 85, 75, 95, 72, 62, 68, 65, 90, 80, 75, 70, 85] + [random.randint(60, 90) for _ in
                                                                                        range(20)],
    'wind_speed': [5, 8, 7, 6, 5, 4, 6, 9, 7, 5, 5, 8, 4, 6, 9, 7, 5] + [random.randint(3, 10) for _ in range(20)],
    'pressure': [1010, 1020, 1005, 1008, 1015, 1012, 1018, 1003, 1014, 1016, 1011, 1015, 1012, 1018, 1003, 1016,
                 1011] + [random.randint(1000, 1020) for _ in range(20)],
}

# Data ko pandas DataFrame format mein convert kiya gaya hai
data = pd.DataFrame(weather_data)


# 2. Data Normalization and Linear Regression Models (Muhammmad Arif)
def normalize_temperature(temp, old_min, old_max, new_min=-50, new_max=50):
    return ((temp - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


min_temp = min(data['temperature'])
max_temp = max(data['temperature'])

# Har ek temperature ko normalize kar ke ek naye column mein save kiya gaya hai
data['normalized_temperature'] = data['temperature'].apply(lambda x: normalize_temperature(x, min_temp, max_temp))

# Features aur target variable define kiya gaya hai
X_temp = data[['humidity', 'wind_speed', 'pressure']]
y_temp = data['normalized_temperature']

# Linear regression models banaye gaye hain
humidity_model = LinearRegression()
wind_speed_model = LinearRegression()
pressure_model = LinearRegression()

# Models ko train kiya gaya hai
humidity_model.fit(y_temp.values.reshape(-1, 1), data[['humidity']])
wind_speed_model.fit(y_temp.values.reshape(-1, 1), data[['wind_speed']])
pressure_model.fit(y_temp.values.reshape(-1, 1), data[['pressure']])


# 3. Prediction Functions (Iman Mirza)
def predict_humidity():
    try:
        input_temp = float(temp_entry.get())
        if input_temp < min_temp or input_temp > max_temp:
            raise ValueError("Temperature out of range.")

        normalized_temp = normalize_temperature(input_temp, min_temp, max_temp)
        prediction = humidity_model.predict([[normalized_temp]])[0][0]
        messagebox.showinfo("Humidity Prediction",
                            f"Based on the given temperature ({input_temp}):\nHumidity: {prediction:.2f}")

    except ValueError:
        messagebox.showerror("Invalid Input",
                             f"Please enter a valid numerical temperature within the range {min_temp} to {max_temp}.")


def predict_wind_speed():
    try:
        input_temp = float(temp_entry.get())
        if input_temp < min_temp or input_temp > max_temp:
            raise ValueError("Temperature out of range.")

        normalized_temp = normalize_temperature(input_temp, min_temp, max_temp)
        prediction = wind_speed_model.predict([[normalized_temp]])[0][0]
        messagebox.showinfo("Wind Speed Prediction",
                            f"Based on the given temperature ({input_temp}):\nWind Speed: {prediction:.2f}")

    except ValueError:
        messagebox.showerror("Invalid Input",
                             f"Please enter a valid numerical temperature within the range {min_temp} to {max_temp}.")


def predict_pressure():
    try:
        input_temp = float(temp_entry.get())
        if input_temp < min_temp or input_temp > max_temp:
            raise ValueError("Temperature out of range.")

        normalized_temp = normalize_temperature(input_temp, min_temp, max_temp)
        prediction = pressure_model.predict([[normalized_temp]])[0][0]
        messagebox.showinfo("Pressure Prediction",
                            f"Based on the given temperature ({input_temp}):\nPressure: {prediction:.2f}")

    except ValueError:
        messagebox.showerror("Invalid Input",
                             f"Please enter a valid numerical temperature within the range {min_temp} to {max_temp}.")


# 4. Data Visualization and Search Functions (Shaheer Riaz)
def visualize_data():
    try:
        input_temp = float(temp_entry.get())
        if input_temp < min_temp or input_temp > max_temp:
            raise ValueError("Temperature out of range.")

        normalized_temp = normalize_temperature(input_temp, min_temp, max_temp)
        filtered_data = data[(data['temperature'] >= input_temp - 5) & (data['temperature'] <= input_temp + 5)]

        plt.figure(figsize=(12, 8))

        plt.subplot(3, 1, 1)
        plt.scatter(filtered_data['temperature'], filtered_data['humidity'], color='blue', s=100, label='Humidity')
        plt.title(f"Temperature vs Humidity (Around {input_temp}\u00b0C)")
        plt.xlabel('Temperature (\u00b0C)')
        plt.ylabel('Humidity (%)')
        plt.grid(True)

        plt.subplot(3, 1, 2)
        plt.scatter(filtered_data['temperature'], filtered_data['wind_speed'], color='orange', s=100,
                    label='Wind Speed')
        plt.title(f"Temperature vs Wind Speed (Around {input_temp}\u00b0C)")
        plt.xlabel('Temperature (\u00b0C)')
        plt.ylabel('Wind Speed (km/h)')
        plt.grid(True)

        plt.subplot(3, 1, 3)
        plt.scatter(filtered_data['temperature'], filtered_data['pressure'], color='green', s=100, label='Pressure')
        plt.title(f"Temperature vs Pressure (Around {input_temp}\u00b0C)")
        plt.xlabel('Temperature (\u00b0C)')
        plt.ylabel('Pressure (hPa)')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid temperature within the range.")


def search_in_range():
    try:
        min_temp = float(min_temp_entry.get())
        max_temp = float(max_temp_entry.get())
        if min_temp < -50 or max_temp > 50:
            raise ValueError("Temperature range out of allowed bounds.")

        results = data[(data['temperature'] >= min_temp) & (data['temperature'] <= max_temp)]
        if not results.empty:
            result_window = tk.Toplevel(root)
            result_window.title("Search Results")

            result_text = tk.Text(result_window, width=80, height=10)
            result_text.pack(padx=10, pady=10)

            result_text.insert(tk.END, f"{'Temperature':<12} {'Humidity':<12} {'Wind Speed':<12} {'Pressure':<12}\n")
            result_text.insert(tk.END, "-" * 50 + "\n")
            for index, row in results.iterrows():
                result_text.insert(tk.END,
                                   f"{row['temperature']:<12} {row['humidity']:<12} {row['wind_speed']:<12} {row['pressure']:<12}\n")
            result_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Search Results", "No data found in the given range.")

    except ValueError:
        messagebox.showerror("Invalid Input",
                             "Please enter valid numerical values for the temperature range within -50 to 50.")


# 5. Model Accuracy and GUI Setup (Ayesha Ahmed)
root = tk.Tk()
root.title("Weather Prediction and Analysis")
icon_path = "C:/Users/CC/PycharmProjects/PythonProject1/icon.ico"  # Replace with your icon file path
root.iconbitmap(icon_path)

temp_frame = tk.Frame(root)
temp_frame.pack(pady=10)

temp_label = tk.Label(temp_frame, text="Enter Temperature:")
temp_label.grid(row=0, column=0, padx=10)
temp_entry = tk.Entry(temp_frame)
temp_entry.grid(row=0, column=1, padx=10)

humidity_button = tk.Button(temp_frame, text="Humidity", command=predict_humidity, width=12, height=1)
humidity_button.grid(row=1, column=0, padx=10, pady=5)
wind_speed_button = tk.Button(temp_frame, text="Wind Speed", command=predict_wind_speed, width=12, height=1)
wind_speed_button.grid(row=1, column=1, padx=10, pady=5)
pressure_button = tk.Button(temp_frame, text="Pressure", command=predict_pressure, width=12, height=1)
pressure_button.grid(row=1, column=2, padx=10, pady=5)

visualize_frame = tk.Frame(root)
visualize_frame.pack(pady=10)
visualize_button = tk.Button(visualize_frame, text="View Weather Trends", command=visualize_data)
visualize_button.pack(padx=10, pady=5)

temp_range_frame = tk.Frame(root)
temp_range_frame.pack(pady=10)
range_label = tk.Label(temp_range_frame, text="Search Temperature Range:")
range_label.grid(row=0, column=0, padx=10)
min_temp_entry = tk.Entry(temp_range_frame, width=10)
min_temp_entry.grid(row=0, column=1, padx=5)
max_temp_entry = tk.Entry(temp_range_frame, width=10)
max_temp_entry.grid(row=0, column=2, padx=5)
range_button = tk.Button(temp_range_frame, text="Search", command=search_in_range)
range_button.grid(row=0, column=3, padx=10)

note_label = tk.Label(root, text="Note: This tool provides approximate predictions and may not be 100% accurate.",
                      fg="red", font=("Arial", 10, "italic"))
note_label.pack(pady=10)

root.mainloop()
