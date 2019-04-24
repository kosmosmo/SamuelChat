import boto3
import json
class Comp():
    def __init__(self,utterance):
        with open('aws.txt') as json_file:
            data = json.load(json_file)
        self.id = data['id']
        self.key = data['key']
        self.utterance = utterance

    def main(self):
        comprehend = boto3.client(service_name='comprehend',
                                  region_name='us-east-1',
                                  aws_access_key_id=self.id,
                                  aws_secret_access_key=self.key)
        text = self.utterance
        lag = json.loads(json.dumps(comprehend.detect_dominant_language(Text=text), sort_keys=True, indent=4))
        flag = False
        for item in lag["Languages"]:
            if item["LanguageCode"] == "en" and item["Score"] >= 0.98:
                flag = True
        if flag:
            comp = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
            return json.loads(comp)
        return None
