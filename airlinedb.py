import os
import sqlite3
from datetime import datetime

#Put console into full screen if tables are wrapping


#creates the tables when program is run
def set_up_db():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()

  #resets all tables when program is run
  curs.execute("DROP TABLE IF EXISTS Aircraft;")
  curs.execute("DROP TABLE IF EXISTS Flight;")
  curs.execute("DROP TABLE IF EXISTS Pilot;")
  curs.execute("DROP TABLE IF EXISTS PilotAssignment;")
  curs.execute("DROP TABLE IF EXISTS MasterTable;")

  #query for Flight table
  flight = """
  CREATE TABLE IF NOT EXISTS Flight (
  FlightID INT,
  DepartureTime DATETIME,
  ArrivalTime DATETIME,
  DepAirport VARCHAR(50),
  ArrAirport VARCHAR(50),
  AircraftID INT,
  PRIMARY KEY (FlightID),
  FOREIGN KEY (AircraftID) REFERENCES Aircraft (AircraftID)
  );"""

  #query for Aircraft table
  aircraft = """
  CREATE TABLE IF NOT EXISTS Aircraft (
  AircraftID INT,
  Model VARCHAR(50),
  Capacity INT,
  PRIMARY KEY (AircraftID)
  );"""

  #query for Pilot table
  pilot = """
  CREATE TABLE IF NOT EXISTS Pilot (
  PilotID INT,
  FirstName VARCHAR(20),
  Surname VARCHAR(20),
  LicenceNumber CHAR(10),
  PRIMARY KEY (PilotID)
  );"""

  #query for PilotAssignment table
  pilotAssignment = """
  CREATE TABLE IF NOT EXISTS PilotAssignment (
  PilotID INT,
  FlightID INT,
  PRIMARY KEY (PilotID, FlightID),
  FOREIGN KEY (PilotID) REFERENCES Pilot (PilotID),
  FOREIGN KEY (FlightID) REFERENCES Flight (FlightID)
  );"""

  #creates all tables
  curs.execute(aircraft)
  curs.execute(pilot)
  curs.execute(pilotAssignment)
  curs.execute(flight)

  conn.commit()
  conn.close()


#inserts the test data into the tables
def insert_test_data():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()
  #test data
  # Insert test data for Aircraft
  curs.execute("INSERT INTO Aircraft VALUES (1, 'Boeing 737', 150);")
  curs.execute("INSERT INTO Aircraft VALUES (2, 'Airbus A320', 180);")
  curs.execute("INSERT INTO Aircraft VALUES (3, 'Boeing 747', 400);")
  curs.execute("INSERT INTO Aircraft VALUES (4, 'Embraer E190', 100);")
  curs.execute("INSERT INTO Aircraft VALUES (5, 'Airbus A380', 600);")

  # Insert test data for Pilot
  curs.execute("INSERT INTO Pilot VALUES (1, 'John', 'Doe', 'P123456789');")
  curs.execute("INSERT INTO Pilot VALUES (2, 'Jane', 'Smith', 'P987654321');")
  curs.execute(
      "INSERT INTO Pilot VALUES (3, 'Mike', 'Johnson', 'P654321987');")
  curs.execute(
      "INSERT INTO Pilot VALUES (4, 'Emily', 'Williams', 'P987654321');")
  curs.execute("INSERT INTO Pilot VALUES (5, 'Alex', 'Jones', 'P654321987');")

  # Insert test data for Flight
  curs.execute("""
  INSERT INTO Flight VALUES (1, '2023-01-01 08:00:00', '2023-01-01 12:00:00', 'Heathrow Airport', 'LAX International', 1)
  ;""")
  curs.execute("""
  INSERT INTO Flight VALUES (2, '2023-01-02 10:30:00', '2023-01-02 15:30:00', 'JFK International', 'Heathrow Airport', 3)
  ;""")
  curs.execute("""
  INSERT INTO Flight VALUES (3, '2023-01-03 12:45:00', '2023-01-03 18:00:00', 'LAX International', 'JFK International', 2)
  ;""")
  curs.execute("""
  INSERT INTO Flight VALUES (4, '2023-01-04 14:00:00', '2023-01-04 18:45:00', 'Dubai International', 'Heathrow Airport', 5);
  """)
  curs.execute("""
  INSERT INTO Flight VALUES (5, '2023-01-05 09:30:00', '2023-01-05 14:00:00', 'Gatwick Airport', 'LAX International', 4);
  """)
  curs.execute("""
  INSERT INTO Flight VALUES (6, '2023-02-01 08:00:00', '2023-01-01 12:00:00', 'Heathrow Airport', 'LAX International', 2)
  ;""")
  curs.execute("""
  INSERT INTO Flight VALUES (7, '2023-02-02 10:30:00', '2023-01-02 15:30:00', 'JFK International', 'Heathrow Airport', 3)
  ;""")
  curs.execute("""
  INSERT INTO Flight VALUES (8, '2023-02-02 10:30:00', '2023-01-02 15:30:00', 'Gatwick Airport', 'Dubai International', 1)
  ;""")

  # Assign pilots to flights
  curs.execute("INSERT INTO PilotAssignment VALUES (1, 1);")
  curs.execute("INSERT INTO PilotAssignment VALUES (2, 1);")
  curs.execute("INSERT INTO PilotAssignment VALUES (2, 2);")
  curs.execute("INSERT INTO PilotAssignment VALUES (3, 3);")
  curs.execute("INSERT INTO PilotAssignment VALUES (1, 4);")
  curs.execute("INSERT INTO PilotAssignment VALUES (4, 4);")
  curs.execute("INSERT INTO PilotAssignment VALUES (5, 5);")
  curs.execute("INSERT INTO PilotAssignment VALUES (4, 5);")
  curs.execute("INSERT INTO PilotAssignment VALUES (3, 5);")
  curs.execute("INSERT INTO PilotAssignment VALUES (5, 6);")
  curs.execute("INSERT INTO PilotAssignment VALUES (1, 7);")
  curs.execute("INSERT INTO PilotAssignment VALUES (2, 8);")
  curs.execute("INSERT INTO PilotAssignment VALUES (3, 8);")

  conn.commit()
  conn.close()


#creates one large table with all information on it
def create_master_table():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()

  # Create MasterTable
  master_table_query = """
  CREATE TABLE IF NOT EXISTS MasterTable AS
  SELECT
      Flight.FlightID,
      Flight.DepartureTime,
      Flight.ArrivalTime,
      Flight.DepAirport,
      Flight.ArrAirport,
      Aircraft.AircraftID,
      Aircraft.Model,
      Aircraft.Capacity,
      Pilot.PilotID,
      Pilot.FirstName,
      Pilot.Surname,
      Pilot.LicenceNumber
  FROM Flight
  LEFT JOIN Aircraft ON Flight.AircraftID = Aircraft.AircraftID
  LEFT JOIN PilotAssignment ON Flight.FlightID = PilotAssignment.FlightID
  LEFT JOIN Pilot ON PilotAssignment.PilotID = Pilot.PilotID;
  """
  curs.execute(master_table_query)
  conn.commit()
  conn.close()


#displays table nicely in console
def display_table(table_name):
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()
  # Get column names
  curs.execute(f"PRAGMA table_info({table_name});")
  columns = [column[1] for column in curs.fetchall()]
  # Get data
  curs.execute(f"SELECT * FROM {table_name}")
  data = curs.fetchall()

  conn.close()

  if not data:
    print(f"No data found in the '{table_name}' table.")
    return

  # Calculate column widths
  col_widths = []
  for i in range(len(columns)):
    column_width = max(len(str(row[i])) for row in data)
    col_widths.append(max(column_width, len(columns[i])) + 1)

  # Print table name
  print(f"{table_name}:")
  # Print header
  header = "|".join(f"{column:<{width}}"
                    for column, width in zip(columns, col_widths))
  print(f"+{'+'.join('-' * (width) for width in col_widths)}+")
  print(f"|{header}|")
  print(f"+{'+'.join('-' * (width) for width in col_widths)}+")

  # Print data
  for row in data:
    # Unpack the row into values
    row_str = "|".join(f"{str(value):<{width}}"
                       for value, width in zip(row, col_widths))
    print(f"|{row_str}|")

  print(f"+{'+'.join('-' * (width) for width in col_widths)}+")


#used to get the choice when there is options
def get_choice(min, max):
  choice = -1
  choiceOk = False
  while not choiceOk:
    try:
      choice = int(input(">> "))

      if min <= choice <= max:
        choiceOk = True
      else:
        print(
            f"Invalid choice. Please enter a number between {min} and {max}.")
    except ValueError:
      print("Invalid choice. Please enter a number.")
  return choice


#the main menu, this is where the user can select what they want to do
def main_menu():
  while True:
    os.system('clear')
    print("Welcome to the Airline Database")
    print("Please select an option:")
    print("1. View all data")
    print("2. View tables")
    print("3. Insert data")
    print("4. Select data")
    print("5. Update data")
    print("6. Delete data")
    print("7. Get statistics")
    print("0. Exit")

    choice = get_choice(0, 7)
    if choice == 1:
      os.system('clear')
      display_all_data()
    elif choice == 2:
      os.system('clear')
      view_tables()
    elif choice == 3:
      os.system('clear')
      insert_data()
    elif choice == 4:
      os.system('clear')
      select_data()
    elif choice == 5:
      os.system('clear')
      update_data()
    elif choice == 6:
      os.system('clear')
      delete_data()
    elif choice == 7:
      os.system('clear')
      get_summary_statistics()
    elif choice == 0:
      os.system('clear')
      break


#displays all the data in one big table
def display_all_data():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()

  create_master_table()
  display_table("MasterTable")
  curs.execute("DROP TABLE IF EXISTS MasterTable")
  conn.commit()
  conn.close()
  print("0. Return to main menu")

  inp = ""
  inpOk = False
  while not inpOk:
    inp = input(">> ")
    if inp == '0':
      inpOk = True
    else:
      print(f"Invalid input. Please enter 0 to return to the main menu.")
  if inp == '0':
    os.system('clear')
    return


#function for displaying table options
def disp_options(action):
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()
  #get table names
  curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
  table_names = [table[0] for table in curs.fetchall()]

  conn.close()
  #print table names
  opts = {}
  print(f"\nSelect the number of the table you wish to {action}:")
  for count, name in enumerate(table_names):
    opts[count + 1] = name
    print(f"{count+1}. {name}")
  print("0. Return back to main menu")

  return opts


#allows the user to select which table to view
def view_tables():
  opts = disp_options("view")
  choice = get_choice(0, len(opts))
  if choice == 0:
    return
  else:
    print("\n")
    display_table(opts[choice])
    print("Would you like to view another table? y/n")
    inpOk = False
    inp = ""
    while not inpOk:
      inp = input(">> ")
      if inp == "y" or inp == "n":
        inpOk = True
      else:
        print("Please enter y or n")

    if inp == "y":
      view_tables()
    else:
      return


#gets types of each column in table
def get_types(table_name):
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()
  curs.execute(f"PRAGMA table_info({table_name});")
  types = [column[2] for column in curs.fetchall()]
  conn.close()
  return types


#checks if datetime input is in the correct format
def validate_datetime(value):
  try:
    datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return True
  except ValueError:
    return False


#checks if input values are the correct types, before executing SQL queries
def validate_inputvals(values, types):
  # Validate types and lengths of user input data before quering
  validated_values = []
  for value, col_type in zip(values, types):
    if col_type.startswith("INT"):
      validated_values.append(int(value))
    elif col_type.startswith("VARCHAR"):
      max_length = int(col_type.split("(")[1].split(")")[0])
      #checks length of input string is less than or equal to the limit
      if len(value) <= max_length:
        validated_values.append(value)
      else:
        print(f"String length should be less than or equal to {max_length}")
        break
    elif col_type.startswith("DATETIME"):
      if validate_datetime(value):
        validated_values.append(value)
      else:
        print("Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS")
    elif col_type.startswith("CHAR"):
      set_length = int(col_type.split("(")[1].split(")")[0])
      #checks string is the required length
      if len(value) == set_length:
        validated_values.append(value)
      else:
        print(f"String length should be equal to {set_length}")
        break
    else:
      raise ValueError("Unsupported data type")
  return validated_values


#allows user to insert data into table
def insert_data():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()
  #display options and get which table the user wants to insert data to
  opts = disp_options("insert data into")
  choice = get_choice(0, len(opts))
  if choice == 0:  #if 0, return back to main menu
    return
  else:
    #otherwise, shows the current table
    print("Current table:")
    display_table(opts[choice])
    types = get_types(opts[choice])

    #gets number of rows user wants to insert, with error handling
    print("How many rows of data do you wish to insert:")
    n = 1
    choiceOk = False
    while not choiceOk:
      try:
        n = int(input(">> "))
        choiceOk = True
      except ValueError:
        print("please enter a valid integer")

    print(f"The required types are: {', '.join(types)}")
    #gets data to insert
    for _ in range(n):
      print("Please enter the data you wish to insert seperated by commas:")
      inpOk = False
      while not inpOk:
        try:
          inp = input(">> ")
          values = list(map(str.strip, inp.split(',')))
          #checks correct number of values have been inputted
          if len(values) == len(types):
            validated_values = validate_inputvals(values, types)
            #Using prepared statement with placeholders to prevent SQL injection
            placeholder = ",".join(["?" for _ in range(len(validated_values))])
            query = f"INSERT INTO {opts[choice]} VALUES ({placeholder})"
            curs.execute(query, validated_values)
            inpOk = True
          else:
            print("Incorrect number of values")
        except sqlite3.OperationalError:
          print("Incorrect input values, try again")
        except sqlite3.IntegrityError:
          print("ID must be unique")
        except ValueError:
          print("Values must be of the right types")
          print(get_types(opts[choice]))

      conn.commit()
      conn.close()
      print("Data inserted.")
      #shows the table with the new data inserted
      print("\nUpdated table:")
      display_table(opts[choice])

    #recalls function if user wants to insert more data, otherwise returns to main menu
    again = ask_again("insert")
    if again == "y":
      os.system('clear')
      insert_data()
    else:
      return


#asks user if they would like to repeat the action
def ask_again(action):
  print(f"Would you like to {action} more data (y/n)")
  choiceOk = False
  choice = ""
  while not choiceOk:
    choice = input(">> ")
    if choice == "y" or choice == "n":
      choiceOk = True
    else:
      print("Please enter y or n")

  return choice


#returns a list of the column headers in given table
def get_cols(table_name):
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()
  curs.execute(f"PRAGMA table_info({table_name});")
  cols = [column[1] for column in curs.fetchall()]
  conn.close()
  return cols


#returns a list of all the values in that column
def get_values_in_col(table_name, col_name):
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()
  curs.execute(f"SELECT {col_name} FROM {table_name};")
  values = [value[0] for value in curs.fetchall()]
  conn.close()
  return values


#allows the user to update data in the tables
def update_data():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()

  #gets which table the user wants to update
  opts = disp_options("update")
  choice = get_choice(0, len(opts))
  if choice == 0:
    return
  else:
    #displays current table
    print("Current table:")
    display_table(opts[choice])

    #select which column to update
    print("Which column do you wish to update:")
    cols = get_cols(opts[choice])
    for count, col in enumerate(cols):
      print(f"{count+1}. {col}")
    col_choice = get_choice(1, len(cols))
    selected_col = cols[col_choice - 1]

    #select which value to update
    print("Which value do you wish to update:")
    values = get_values_in_col(opts[choice], selected_col)
    for count, value in enumerate(values):
      print(f"{count+1}. {value}")
    val_choice = get_choice(1, len(values))
    selected_val = values[val_choice - 1]
    row_id = val_choice
    types = get_types(opts[choice])

    # check if user wants to update all instances or just one if theres more than one instance of a value
    all_instances = False
    if values.count(selected_val) > 1:
      print(
          "Would you like to update all instances of this value in this table (y/n)"
      )
      inpOk = False
      inp = ""
      while not inpOk:
        inp = input(">> ")
        if inp == "y" or inp == "n":
          inpOk = True
        else:
          print("Please enter y or n")

      if inp == "y":
        all_instances = True

    #get new value
    print("Please enter the new value: ")
    inpOk = False
    while not inpOk:
      try:
        new_val = input(">> ")
        #check input value is the right type
        validated = validate_inputvals([new_val], [types[col_choice - 1]])
        #prepare query
        placeholder = "?"
        if all_instances:
          query = f"UPDATE {opts[choice]} SET {selected_col} = {placeholder} WHERE {selected_col} = '{selected_val}';"
        else:
          query = f"UPDATE {opts[choice]} SET {selected_col} = {placeholder} WHERE ROWID = {row_id};"
        #execute query
        curs.execute(query, validated)
        inpOk = True
      except sqlite3.OperationalError:
        print("Incorrect input value, try again")
      except sqlite3.IntegrityError:
        print("ID must be unique")
      except sqlite3.ProgrammingError:
        print("Incorrect input value, try again")
      except ValueError:
        print("Values must be of the right types")

    conn.commit()
    conn.close()
    #displays table with updated data
    print("Table updated")
    print("\nUpdated table:")
    display_table(opts[choice])

    #check if user would like to update more data, otherwise returns to main menu
    again = ask_again("update")
    if again == "y":
      os.system('clear')
      update_data()
    else:
      return


#allows user to select specific data from the tables
def select_data():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()
  create_master_table()
  columns = get_cols("MasterTable")

  print("\nSelect columns to display (comma-separated):")
  print("0. Main menu")
  print("Available columns:")
  for count, col in enumerate(columns):
    print(f"{count + 1}. {col}")

  # Get user-selected columns and validate
  inpOk = False
  selected_columns_indexes = []
  while not inpOk:
    inp = input(">> ")
    if inp == "0":
      return
    selected_columns_indexes = list(map(int, inp.split(',')))
    # Validate selected column indexes
    if any(index < 1 or index > len(columns)
           for index in selected_columns_indexes):
      print("Invalid column selection. Please select valid columns.")
    else:
      inpOk = True

  selected_columns = [columns[index - 1] for index in selected_columns_indexes]

  #Get the WHERE clause
  print("\nEnter the WHERE clause (or press Enter for no WHERE clause):")
  print("Seperate multiple conditions with AND")
  whereOk = False
  maybe_where = ""
  while not whereOk:
    try:
      maybe_where = input("WHERE: ")
      where_clause = f"WHERE {maybe_where}" if maybe_where else ""
      #prepare query
      query = f"SELECT {','.join(selected_columns)} FROM MasterTable {where_clause}"
      #Execute query
      curs.execute(query)
      whereOk = True
    except sqlite3.OperationalError:
      print("Incorrect where clause")
      print(
          "Possible errors, no quotations around value, misspelled column name, spelling errors, etc."
      )
      print("Please try again")

  #get results and display them
  result = curs.fetchall()
  print("\nResults:")
  display_table_from_result(result, selected_columns)

  curs.execute("DROP TABLE IF EXISTS MasterTable")
  conn.commit()
  conn.close()

  #check if user would like to select more data, otherwise returns to main menu
  again = ask_again("select")
  if again == "y":
    os.system('clear')
    select_data()
  else:
    return


#displays result of select nicely
def display_table_from_result(result, columns):
  # Display the selected data
  if not result:
    print("No data found.")
    return
  col_widths = []
  for i in range(len(columns)):
    column_width = max(len(str(col)) for col in columns)
    col_widths.append(column_width + 7)

  # Print header
  header = "|".join(f"{column:<{width}}"
                    for column, width in zip(columns, col_widths))
  print(f"+{'+'.join('-' * (width) for width in col_widths)}+")
  print(f"|{header}|")
  print(f"+{'+'.join('-' * (width) for width in col_widths)}+")

  # Print data
  for row in result:

    row_str = "|".join(f"{str(value):<{width}}"
                       for value, width in zip(row, col_widths))
    print(f"|{row_str}|")

  print(f"+{'+'.join('-' * (width) for width in col_widths)}+")


#allow user to delete data from tables
def delete_data():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()

  #gets which table the user wants to delete from
  opts = disp_options("delete from")
  choice = get_choice(0, len(opts))
  if choice == 0:
    return
  else:
    #displays current table
    print("Current table:")
    display_table(opts[choice])
    #gets the number of rows in the selected table
    row_count = curs.execute(
        f"SELECT COUNT(*) FROM {opts[choice]}").fetchone()[0]

    #select which row to delete
    print("Which row do you wish to delete (enter row number):")
    inpOk = False
    row_id = ""
    while not inpOk:
      try:
        row_id = int(input(">> "))
        if row_id < 1 or row_id > row_count:
          print("Invalid row selection. Please select valid row.")
        else:
          inpOk = True
      except ValueError:
        print("Invalid input. Please enter a valid row number.")

    #Create and execute query
    query = f"DELETE FROM {opts[choice]} WHERE ROWID = {row_id};"
    curs.execute(query)

    conn.commit()
    conn.close()

    #displays table with updated data
    print("Table updated")
    print("\nUpdated table:")
    display_table(opts[choice])

    #check if user would like to update more data, otherwise returns to main menu
    again = ask_again("delete")
    if again == "y":
      os.system('clear')
      delete_data()
    else:
      return


#checks if input date is in the correct format
def validate_date(value):
  try:
    datetime.strptime(value, '%Y-%m-%d')
    return True
  except ValueError:
    return False


#allows the user to get some summary statistics
def get_summary_statistics():
  conn = sqlite3.connect("AirlineDB")
  curs = conn.cursor()

  # Print the options for summary statistics
  print("Select the summary statistic you want to view:")
  print("0. Main menu")
  print("1. Number of flights in a specific week")
  print("2. Number of flights to a specific destination per month")
  print("3. Number of flights from a specific destination per month")
  print("4. Number of pilots on a flight")

  choice = get_choice(0, 4)

  # Return to main menu if choice is 0
  if choice == 0:
    return

  elif choice == 1:
    print("Enter the start of the week (format: YYYY-MM-DD):")
    #Validate the date input
    while True:
      week = input(">> ")
      if validate_date(week):
        break
      else:
        print("Enter a valid date (format: YYYY-MM-DD)")

    # Query for getting the count of flights in a specific week
    query = f"SELECT COUNT(*) FROM Flight WHERE DepartureTime >= date('{week}') AND DepartureTime < date('{week}', '+7 days');"
    curs.execute(query)
    result = curs.fetchone()[0]
    print(f"Number of flights in the specific week: {result}\n")

  elif choice == 2:
    print("Enter the destination airport:")
    while True:
      destination = input(">> ")
      # Query for checking airport existence
      airport_exists_query = f"SELECT COUNT(*) FROM Flight WHERE ArrAirport = ? OR DepAirport = ?;"
      curs.execute(airport_exists_query, (
          destination,
          destination,
      ))
      result = curs.fetchone()[0]
      if result == 0:
        print(
            "Airport does not exist. Please enter a valid destination airport."
        )
      else:
        break

      # Query for getting number of flights per month to input airport
    query = f"SELECT strftime('%m', DepartureTime) as month, COUNT(*) as num_flights FROM Flight WHERE ArrAirport = ? GROUP BY month;"
    curs.execute(query, (destination, ))
    results = curs.fetchall()

    # Print the results
    print("\nNumber of flights to the specific destination per month:")
    for month, num_flights in results:
      print(f"Month: {month}, Number of Flights: {num_flights}")
    print("\n")

  elif choice == 3:
    print("Enter the departure airport:")
    while True:
      departure = input(">> ")
      # Query for checking airport existence
      airport_exists_query = f"SELECT COUNT(*) FROM Flight WHERE ArrAirport = ? OR DepAirport = ?;"
      curs.execute(airport_exists_query, (
          departure,
          departure,
      ))
      result = curs.fetchone()[0]
      if result == 0:
        print(
            "Airport does not exist. Please enter a valid departure airport.")
      else:
        break

      # Query for getting number of flights per month from input airport
    query = f"SELECT strftime('%m', DepartureTime) as month, COUNT(*) as num_flights FROM Flight WHERE DepAirport = ? GROUP BY month;"
    curs.execute(query, (departure, ))
    results = curs.fetchall()

    # Print the results
    print("\nNumber of flights from the specific destination per month:")
    for month, num_flights in results:
      print(f"Month: {month}, Number of Flights: {num_flights}")
    print("\n")

  elif choice == 4:
    print("Enter the FlightID:")
    while True:
      flight_id = input(">> ")
      # Query for checking flight number existence
      flight_exists_query = f"SELECT COUNT(*) FROM Flight WHERE FlightID = ?;"
      curs.execute(flight_exists_query, (flight_id, ))
      result = curs.fetchone()[0]
      if result == 0:
        print("Flight number does not exist. Please enter a valid FlightID")
      else:
        break

    #query for getting number of pilots on a flight
    query = f"SELECT COUNT(*) FROM PilotAssignment WHERE FlightID = ?;"
    curs.execute(query, (flight_id, ))
    result = curs.fetchone()[0]
    print(f"Number of pilots on flight {flight_id}: {result}\n")

  conn.close()

  # Ask if user wants to get statistics again
  again = ask_again("get statistics of")
  if again == "y":
    os.system('clear')
    get_summary_statistics()
  else:
    return


#tables are set up, and test data is inserted and then main menu is shown
set_up_db()
insert_test_data()
main_menu()
