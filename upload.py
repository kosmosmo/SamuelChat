import boto3
from botocore.client import Config
import os,json,collections
class s3upload():
    def __init__(self,direct):
        with open('aws.txt') as json_file:
            data = json.load(json_file)
        self.id = data['id']
        self.key = data['key']
        self.bucket = 'samuelchat'
        self.direct = direct

    def run(self):
        files = os.listdir(self.direct)
        res = collections.defaultdict(str)
        for f in files:
            data = open(self.direct + f, 'rb')

            s3 = boto3.resource(
                's3',
                aws_access_key_id=self.id,
                aws_secret_access_key=self.key,
                config=Config(signature_version='s3v4')
            )
            s3.Bucket(self.bucket).put_object(Key=f, Body=data)
            s3.Bucket(self.bucket).Object(f).Acl().put(ACL='public-read')
            res[f[:-4]] = "https://s3.amazonaws.com/" + self.bucket + '/' + f
            print (f)

        with open('soundmap.json', 'w') as outfile:
            json.dump(res, outfile)
