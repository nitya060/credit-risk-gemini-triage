import pandas as pd

print("Fetching the real-world credit dataset...")

# Download the real bank credit dataset from the public link
url = "https://raw.githubusercontent.com/YBIFoundation/Dataset/main/Credit%20Default.csv"
df = pd.read_csv(url)

# Save it directly into your 'data' folder
df.to_csv("data/raw_credit_data.csv", index=False)

print("Success! The dataset is now saved inside your 'data' folder.")

print("Here are the first few rows of your data:")
print(df)
