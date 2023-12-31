import gspread
from oauth2client.service_account import ServiceAccountCredentials


def init():
    global sheet
    # Set up Google Sheets API credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet by title
    sheet_title = "Whats"
    sheet = client.open(sheet_title).sheet1  # Use the appropriate sheet index if not the first sheet


def write_sheet():
    global sorted_data
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

    sheet.update("A1:E" + str(len(sorted_data)), sorted_data)

    # Clear the existing data in the sheet
#sheet.clear()


def readMyMsgAtCol(column_to_search):

    # Update the sheet with the sorted data
    
    # Loop over each row in the specified column until finding the first non-empty cell
    row = 1
    cell = None

    # Set the maximum row to iterate over
    max_row = 11

    while not cell and row <= max_row:
        # Find the cell in the current row
        cell = sheet.cell(row, column_to_search)

        # Check if the cell is empty
        if not cell.value:
            cell = None  # Reset cell to None if the cell is empty
            row += 1  # Move to the next row
    print(row)

    if row == 12:
        return False

    # Prepare the information as a string
    cell_info = f"The first non-empty cell in column {column_to_search} is at row {cell.row}, column {cell.col}, and has the value: {cell.value}"

    cell_chat = sheet.cell(cell.row,2)

    # Print the information to the console
    print(cell_info)

    # Write the information to a text file
    # This writes the last text appearing on a chat and the message that we want to send
    with open("write_CMD.txt", "w", encoding="utf-8") as file:
        file.write(str(cell_chat.value) + "|" + str(cell.value))


    cell_chatName = sheet.cell(cell.row,1)
    cell_date = sheet.cell(cell.row,4)

    # This writes the chat name to a file in case that the last text appearing has some emojis or something weird in it
    # so we have 2 ways to search for our wanted chat
    with open("write_CMD_chatName.txt", "w", encoding="utf-8") as file:
        file.write(str(cell_chatName.value))


    with open("write_CMD_date.txt", "w", encoding="utf-8") as file:
        file.write(str(cell_date.value))


    return True


def delete_col(col):
    # Specify the column number you want to delete (e.g., column B)
    column_to_delete = col  # Change this to your desired column number

    # Get the number of rows in the sheet
    num_rows = sheet.row_count

    # Create an empty list to store the new values for the specified column
    empty_column_values = [[""] * num_rows]

    # Create a ValueRange object with the empty values
    value_range = {"values": empty_column_values}

    # Specify the range to update (e.g., "B1:B" for column B)
    range_to_update = f"{chr(ord('A') + column_to_delete - 1)}1:{chr(ord('A') + column_to_delete)}{num_rows}"

    # Update the specified range with the empty values
    sheet.values_update(range_to_update, params=value_range)

