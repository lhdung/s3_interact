import os
import boto3


class S3Handler():
    def __init__(self, aws_access_key, aws_secret_key, region_name):
        self.s3 = boto3.client('s3', 
                                region_name=region_name, 
                                aws_access_key_id=aws_access_key, 
                                aws_secret_access_key=aws_secret_key)

    def list_buckets(self):
        reponse = self.s3.list_buckets()
        if 'Buckets' in reponse:
            print("S3 Buckets:")
            for bucket in reponse['Buckets']:
                print(f" - {bucket['Name']}")
        else:
            print("No buckets found.")
        return reponse
    
        
    def list_objects(self, bucket_name):
        files = self.s3.list_objects_v2(Bucket=bucket_name)
        for file in files['Contents']:
            print(f" - {file['Key']}")
        return files

    def download_file(self, file_name, bucket):
        self.s3.download_file(bucket, file_name, file_name)

    def delete_file(self, bucket, file_name ):
        if self.s3.delete_object(Bucket=bucket, Key=file_name):
            print("File deleted successfully.")
        else:
            print("File not found.")

    
    def check_duplicate(self, bucket_name, file_name):
        files = self.s3.list_objects(Bucket=bucket_name)
        for file in files['Contents']:
            if file['Key'] == file_name:
                print("Found duplicate file in buckets: ", file['Key'])
                return True
        print("No duplicate found")
        return False

    def upload_file(self, bucket_name, file_obj, file_name):
        if not self.check_duplicate(bucket_name, file_name):
            try:
                print("Uploading file...")
                self.s3.upload_fileobj(file_obj, bucket_name, file_name)
                print("File uploaded successfully.")
                return True
            except Exception as e:
                print(f"Error uploading file: {e}")
                return False
        else:
            print("Duplicate file found. Exiting...")
            return False


# if __name__ == '__main__':
#     s3 = S3Handler()
#     # s3.list_buckets()
#     # s3.list_objects("auto-python")
#     s3.upload_file("auto-python", "C:\\Users\\Dung.LeH\\Desktop\\repo\\exercises\\upload\\data\\azure.png")
#     s3.delete_file(bucket="auto-python", file_name="azure.png")
