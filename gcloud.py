import re
import subprocess

class GoogleCloud():
    def __init__(self, project, location, bucket, instance, database, database_path):
        self.project = project
        self.location = location
        self.bucket = "gs://{}".format(bucket)
        self.instance = instance
        self.database = database
        self.database_path = database_path

    def create_bucket(self):
        """
        Creates a bucket using Popen. 
        Output is bound to stderr not stdout
        """
        process = subprocess.Popen(['gsutil', 'mb', '-p', self.project, '-l', self.location, self.bucket], stderr=subprocess.PIPE)
        output = process.stderr.read()
        return output

    def find_service_account(self):
        """
        Find Service Account Address
        Output is bound to stdout not stderr
        """
        process = subprocess.Popen(['gcloud', 'sql', 'instances', 'describe', self.instance], stdout=subprocess.PIPE)
        output = process.stdout.read()
        service_account_address = re.findall(r'[\w\.-]+@[\w\.-]+', output)
        return("{}:W".format(service_account_address[0]))

    def grant_bucket_permissions(self):
        """
        Use Service Account Address to Grant Permissions
        Output is bound to stderr not stdout
        """
        service_account_string = self.find_service_account()
        process = subprocess.Popen(['gsutil', 'acl', 'ch', '-u', service_account_string, self.bucket], stderr=subprocess.PIPE)
        output = process.stderr.read()
        return output
    
    def export_database(self):
        """
        Export a database
        Output is bound to stdout not stderr
        """
        path_to_database = "{}/{}".format(self.bucket, self.database_path)
        process = subprocess.Popen(['gcloud', 'sql', 'export', 'sql', self.instance, path_to_database, '--database='+self.database], stdout=subprocess.PIPE)
        output = process.stdout.read()
        return output

    def import_database(self):
        """
        Import a database
        Output is bound to stdout not stderr
        """
        path_to_database = "{}/{}".format(self.bucket, self.database_path)
        process = subprocess.Popen(['gcloud', 'sql', 'import', 'sql', self.instance, path_to_database, '--database='+self.database], stdout=subprocess.PIPE)
        output = process.stdout.read()
        return output
