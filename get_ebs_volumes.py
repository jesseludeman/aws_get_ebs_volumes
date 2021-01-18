import boto3
import csv
import argparse

def get_ebs_volumes(ec2):
    """
    Retrieves all EBS volumes with status 'available' and 'size'.
    Any volume with this status are NOT connected to an EC2 instance and can be safely deleted.
    Returns a nested list.
    """
    
    # Empty list for EBS volumes
    unattachedVolumes = [[],[]]

    # Get 'available' EBS volumes, which are not attached to any instance
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}], DryRun=False)

    # Iterate through the collection of EBS volumes
    try:
        for volume in volumes["Volumes"]:
            unattachedVolumes[0].append(volume["VolumeId"])
            unattachedVolumes[1].append(volume["Size"])
    except Exception as e:
        print("No unattached volumes found", e)

    return unattachedVolumes

def generate_csv_report(ec2):
    """
    Generates a CSV report of all unattached EBS volumes for the current AWS account in the current working directory.
    Appends the 'available' and 'size' results into two (2) separate columns for readability and reporting purposes.
    """

    volumes = get_ebs_volumes(ec2)

    with open("VolumeIDS.csv", "w", newline="", encoding="utf-8") as output:
        headers = ["Volume IDs", "Size"]
        writer = csv.writer(output)

        writer.writerow(headers)
        writer.writerows(zip(volumes[0], volumes[1]))

def delete_unattached_ebs_volumes(ec2):
    """
    Iterates through the list of EBS volumes, and performs a delete operation on each volume.
    Returns the volumes nested list if no volumes are found.
    """

    # Store the volumes to be deleted here
    volumes = get_ebs_volumes(ec2)

    # Delete the volumes
    try:
        for volume in volumes[0]:
            for size in volume[1]:
                print("Deleting " + volume)
                ec2.delete_volume(VolumeId=volume)
    except Exception as exc:
        # Return the list 
        return volumes

if __name__ == "__main__":
    # Establish EC2 session, and set the region
    ec2 = boto3.client("ec2", region_name="ap-southeast-2")

    # Call the functions here
    get_ebs_volumes(ec2)
    generate_csv_report(ec2)
    delete_unattached_ebs_volumes(ec2)