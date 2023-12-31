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
sorted_data.insert(0, ["Name", "Msg", "Sender", "Date"])

# Clear the existing data in the sheet
#sheet.clear()

# Update the sheet with the sorted data
sheet.update("A1:E" + str(len(sorted_data)), sorted_data)

# Specify the column to search (let's say column E)
column_to_search = 5

# Loop over each row in the specified column until finding the first non-empty cell
row = 1
cell = None

while not cell:
    # Find the cell in the current row
    cell = sheet.cell(row, column_to_search)

    # Check if the cell is empty
    if not cell.value:
        cell = None  # Reset cell to None if the cell is empty
        row += 1  # Move to the next row

# Prepare the information as a string
cell_info = f"The first non-empty cell in column {column_to_search} is at row {cell.row}, column {cell.col}, and has the value: {cell.value}"

cell_chat = sheet.cell(cell.row,1)

# Print the information to the console
print(cell_info)

# Write the information to a text file
with open("write_CMD.txt", "w", encoding="utf-8") as file:
    file.write(str(cell_chat.value) + "|" + str(cell.value))
