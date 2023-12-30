import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet by title
sheet_title = "Whats"
sheet = client.open(sheet_title).sheet1  # Use the appropriate sheet index if not the first sheet

# Read data from external files
with open("output.txt", "r", encoding="utf-8") as file:
    output_data = [line.strip() for line in file.readlines()]

with open("msg.txt", "r", encoding="utf-8") as file:
    msg_data = [line.strip() for line in file.readlines()]

with open("sender.txt", "r", encoding="utf-8") as file:
    sender_data = [line.strip() for line in file.readlines()]

with open("date.txt", "r", encoding="utf-8") as file:
    date_data = [line.strip() for line in file.readlines()]

# Ensure both lists have the same length
if len(output_data) != len(msg_data) != len(sender_data) != len(date_data):
    raise ValueError("All lists must have the same length")

# Combine data into a list of lists
combined_data = list(zip(output_data, msg_data, sender_data, date_data))

# Sort combined data based on the "Date" column (assuming "Date" is the fourth column, index 3)
sorted_data = sorted(combined_data, key=lambda x: x[3], reverse=True)

# Insert header row
sorted_data.insert(0, ["Name", "Msg", "Sender", "Date", "Write_CMD"])

# Clear the existing data in the sheet
#sheet.clear()

# Update the sheet with the sorted data
sheet.update("A1:E" + str(len(sorted_data)), sorted_data)
