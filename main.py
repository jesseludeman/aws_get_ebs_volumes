import boto3
import csv
import argparse


def get_ebs_volumes(ec2):
    """
    Retrieves all EBS volumes with status 'available' and 'size'
    Volumes that have this criteria not connected to an EC2 instance and can be safely deleted
    """

    # Empty list for EBS volumes
    unattached_volumes = [[], []]

    # Get 'available' EBS volumes, which are not attached to any instance
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}], DryRun=False)

    # Iterate through the collection of EBS volumes
    try:
        for volume in volumes["Volumes"]:
            unattached_volumes[0].append(volume["VolumeId"])
            unattached_volumes[1].append(volume["Size"])
    except Exception as error:
        print("No unattached volumes found", error)

    return unattached_volumes


def generate_csv_report(ec2):
    """
    Generates a report in CSV format of all unattached EBS volumes
    """

    volumes = get_ebs_volumes(ec2)

    with open("volumeIDs.csv", "w", newline="", encoding="utf-8") as output:
        headers = ["Volume IDs", "Size"]
        writer = csv.writer(output)

        writer.writerow(headers)
        writer.writerows(zip(volumes[0], volumes[1]))


def delete_volumes(ec2):
    """
    Iterates through the list of EBS volumes, and performs a delete operation on each volume
    """

    # Store the volumes to be deleted here
    volumes = get_ebs_volumes(ec2)

    # Delete the volumes
    try:
        for volume in volumes[0]:
            for size in volume[1]:
                print("Deleting " + volume)
                ec2.delete_volume(VolumeId=volume)
    except Exception as error:
        return volumes


if __name__ == "__main__":
    # Establish EC2 session, and set the region
    ec2 = boto3.client("ec2", region_name="ap-southeast-2")

    # Setup argparse here to enable command line functionality with parameters and arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generate-csv", help="Generates a report for the existing EBS volumes in CSV format", action="store_true")
    parser.add_argument(
        "--delete", help="Deletes the listed EBS volumes", action="store_true")
    args = parser.parse_args()

    if args.generate_csv:
        generate_csv_report(ec2)
    if args.delete:
        delete_volumes(ec2)
