import boto3
import csv
import io
import json
import urllib.parse
from datetime import datetime, timezone

s3 = boto3.client("s3")

REQUIRED_COLUMNS = ["Name", "Age", "City", "Salary"]


def lambda_handler(event, context):

    print("ETL Lambda started")

    for record in event.get("Records", []):

        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        print(f"Processing file: s3://{bucket}/{key}")

        # Process only CSV files inside raw/
        if not key.startswith("raw/") or not key.lower().endswith(".csv"):
            print(f"Skipping file: {key}")
            continue

        start_time = datetime.now(timezone.utc)

        try:
            # Read raw CSV from S3
            response = s3.get_object(
                Bucket=bucket,
                Key=key
            )

            content = response["Body"].read().decode("utf-8")

            reader = csv.DictReader(io.StringIO(content))

            # Check required columns
            if not reader.fieldnames:
                raise ValueError("CSV file has no header")

            missing_columns = [
                col for col in REQUIRED_COLUMNS
                if col not in reader.fieldnames
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}"
                )

            valid_rows = []
            invalid_rows = []

            seen_records = set()

            total_records = 0
            invalid_count = 0

            # Validate every row
            for line_number, row in enumerate(reader, start=2):

                total_records += 1

                name = (row.get("Name") or "").strip()
                age = (row.get("Age") or "").strip()
                city = (row.get("City") or "").strip()
                salary = (row.get("Salary") or "").strip()

                reason = None

                # Missing fields
                if not name:
                    reason = "Missing Name"

                elif not age:
                    reason = "Missing Age"

                elif not city:
                    reason = "Missing City"

                elif not salary:
                    reason = "Missing Salary"

                # Validate Age
                elif not age.isdigit() or int(age) <= 0:
                    reason = "Invalid Age"

                # Validate Salary
                else:
                    try:
                        salary_value = float(salary)

                        if salary_value < 0:
                            reason = "Invalid Salary"

                    except ValueError:
                        reason = "Invalid Salary"

                # Standardize data
                standardized_name = name.title()
                standardized_city = city.title()

                # Duplicate detection
                fingerprint = (
                    standardized_name,
                    age,
                    standardized_city,
                    salary
                )

                if reason is None and fingerprint in seen_records:
                    reason = "Duplicate record"

                if reason is None:

                    seen_records.add(fingerprint)

                    valid_rows.append({
                        "Name": standardized_name,
                        "Age": int(age),
                        "City": standardized_city,
                        "Salary": float(salary)
                    })

                else:

                    invalid_count += 1

                    invalid_rows.append({
                        "Name": name,
                        "Age": age,
                        "City": city,
                        "Salary": salary,
                        "Reason": reason,
                        "Line": line_number
                    })

            # Get original filename
            filename = key.split("/")[-1]

            if filename.lower().endswith(".csv"):
                base_name = filename[:-4]
            else:
                base_name = filename

            # ------------------------------------------------
            # SAVE VALID DATA
            # ------------------------------------------------

            processed_key = (
                f"processed/{base_name}_processed.csv"
            )

            processed_output = io.StringIO()

            writer = csv.DictWriter(
                processed_output,
                fieldnames=[
                    "Name",
                    "Age",
                    "City",
                    "Salary"
                ]
            )

            writer.writeheader()
            writer.writerows(valid_rows)

            s3.put_object(
                Bucket=bucket,
                Key=processed_key,
                Body=processed_output.getvalue().encode("utf-8"),
                ContentType="text/csv"
            )

            print(
                f"Processed file created: {processed_key}"
            )

            # ------------------------------------------------
            # SAVE INVALID DATA
            # ------------------------------------------------

            invalid_key = (
                f"invalid/{base_name}_invalid.csv"
            )

            invalid_output = io.StringIO()

            invalid_writer = csv.DictWriter(
                invalid_output,
                fieldnames=[
                    "Name",
                    "Age",
                    "City",
                    "Salary",
                    "Reason",
                    "Line"
                ]
            )

            invalid_writer.writeheader()
            invalid_writer.writerows(invalid_rows)

            s3.put_object(
                Bucket=bucket,
                Key=invalid_key,
                Body=invalid_output.getvalue().encode("utf-8"),
                ContentType="text/csv"
            )

            print(
                f"Invalid file created: {invalid_key}"
            )

            # ------------------------------------------------
            # SAVE METADATA
            # ------------------------------------------------

            end_time = datetime.now(timezone.utc)

            metadata = {
                "file_name": filename,
                "source_key": key,
                "processing_time": end_time.isoformat(),
                "total
