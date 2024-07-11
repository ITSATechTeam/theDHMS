import csv
from django.contrib.auth.models import User  # Import User model if not already imported
from userarea.models import StaffDataSet  # Adjust accordingly to import your StaffDataSet model

def delete_duplicate_emails_and_save_to_database(csv_file_path):
    # Step 1: Read the CSV file
    with open(csv_file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)  # Read all rows into a list

    # Step 2: Identify rows with duplicate emails and prepare to delete them
    seen_emails = set()
    rows_to_delete = []

    for i, row in enumerate(data):
        if i == 0:  # Skip header row
            continue
        
        email = row[17]  # Assuming email is in column 17 (adjust index as per your CSV structure)

        if email in seen_emails:
            rows_to_delete.append(i)  # Collect index of rows to delete
        else:
            seen_emails.add(email)

    # Step 3: Delete duplicate rows from the data list
    rows_to_delete.reverse()  # Reverse to delete from end to start
    for idx in rows_to_delete:
        data.pop(idx)

    # Step 4: Save back to the database
    # Connect to your database and perform deletion and insertion
    for row in data[1:]:  # Skip header row when iterating over data
        email = row[17]  # Assuming email is in column 17 (adjust index as per your CSV structure)

        # Delete existing records with the email from StaffDataSet and User models
        StaffDataSet.objects.filter(staff_email=email).delete()
        User.objects.filter(email=email).delete()

        # Insert new records into StaffDataSet and User models
        # Assuming you have appropriate fields in StaffDataSet and User models
        staff_data = StaffDataSet(staff_email=email)
        staff_data.save()

        user_data = User(email=email)
        user_data.save()

    print("Duplicate rows deleted and data saved back to the database.")

# Example usage:
csv_file_path = 'path/to/your/data.csv'
delete_duplicate_emails_and_save_to_database(csv_file_path)
