import os
class bulkConverter():
    def __init__(self,direct,target):
        self.direct = direct
        self.target = target
    def main(self):
        files = os.listdir(self.direct)
        for f in files:
            if f.lower()[-3:] == "mp3":
                print (f)
                self.process(f)

    def process(self,f):
        inFile = self.direct + f
        outFile = self.target + f.replace(' ', '')
        cmd = "ffmpeg -i {} -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 {}".format(inFile, outFile)
        os.popen(cmd)

