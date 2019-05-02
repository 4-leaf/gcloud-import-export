from gcloud import GoogleCloud
from terminal import bcolors
color = bcolors

"""
ALL OF THE DIALOG IS HERE
"""

instance_name = raw_input(color.BOLD + "What is Your Instance Name: " + color.ENDC + "\nInstance Name: ")
project = raw_input(color.BOLD + "What is the name of your project (usually ends with -hzdg): "+ color.ENDC + "\nProject Name: ")
need_bucket = raw_input(color.BOLD + "Will you need to create a bucket?" + color.ENDC + "\ny/n: ")
import_or_export = raw_input(color.BOLD + "Are you importing or exporting a database ?" + color.ENDC +"\nimport/export: ")

if need_bucket.lower() == "y":
    print("\n" + color.OKGREEN + "Bucket Creation: " + color.ENDC)
    bucket_name = raw_input("Name your bucket: ")
    bucket_location = raw_input("Bucket location? (usually " +color.OKBLUE + "us-east1" + color.ENDC +" ): ")
else:
    bucket_location = ""
    bucket_name = ""

if import_or_export.lower() == "export":
    print("\n" + color.OKGREEN + "Exporting DB: " + color.ENDC)
    database_name = raw_input("Name of DB to Export: ")
    database_path = raw_input("Backup Name ( "+ color.OKBLUE +"include .sql or .gz"+ color.ENDC + " ): ")
    if bucket_name:
        pass
    else:
        bucket_name = raw_input("Your Bucket Name: ")
else:
    print("\n" + color.OKGREEN + "Importing DB: " + color.ENDC)
    database_name = raw_input("DB to import into: ")
    database_path = raw_input("Name of DB to Import: ")
    if bucket_name:
        pass
    else:
        bucket_name = raw_input("Your Bucket Name: ")

"""
END OF DIALOG
"""
GoogleCloud = GoogleCloud(project, bucket_location, bucket_name, instance_name, database_name, database_path)

if need_bucket == "y":
    print(GoogleCloud.create_bucket())
    print(GoogleCloud.grant_bucket_permissions())

if import_or_export == "export":
    print(GoogleCloud.export_database())
else:
    print(GoogleCloud.import_database())

