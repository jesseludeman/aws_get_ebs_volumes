## Introduction
Wrote this to automate removing unattached EBS volumes for a previous role. The role in question had thousands of unattached volumes across multiple AWS accounts, and I couldn't be bothered doing it manually.

## Prerequisites and requirements
- Python 3
- AWS CLI
- Boto3
- A valid AWS access key and secret

## Usage
To retrieve all unattached volumes:
`python3 main.py --generate-csv`

To delete all unattached volumes:
`python3 main.py --delete`

## To do
- Change data structure of `unattached_volumes` as I don't like nested lists. Consider using a dictionary nested inside a list.
- Prompt user to delete the volumes as this is destructive.