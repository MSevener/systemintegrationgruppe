import boto3
import urllib2
import os.path

s3 = boto3.client('s3')

bucketname ="systemintegration"
dummy = "src/dummy.jpg"

def addImageFromUrl(key, url):
    data = urllib2.urlopen(url).read()
    try:
        print "put " + key
        s3.put_object(Bucket=bucketname, Key = key, Body = data, ContentType = "image/jpg")
    except Exception as e:
        print e

def getImagePath(key, alternativePath):
    imageStream = ""
    imagePath = ""
    bucketkey = "src/" + key + ".jpg"
    s3ElementPath = "https://s3.amazonaws.com/" + bucketname + "/src/" + key + ".jpg"
    pictureAvailable = 0
    try:
        imageStream = s3.get_object(Bucket=bucketname,Key = bucketkey)
        imagePath = s3ElementPath
        pictureAvailable = 1
    except Exception as e:
        print "Nehme alternativen Pfad"
    if pictureAvailable == 0:
        if alternativePath != '':
            addImageFromUrl(bucketkey, alternativePath)
            imagePath = alternativePath
        else:
            imagePath = "https://s3.amazonaws.com/" + bucketname + "/src/dummy.jpg"
    print imagePath
    return imagePath

def getThumbnailImg(key):
    newPath= "https://s3.amazonaws.com/" + bucketname + "/thumbnail/" + key + ".jpg"
    thumbnail = "<img src = \"" + newPath + "\" onError=\"this.src = 'https://s3.amazonaws.com/" + bucketname + "/thumbnail/dummy.jpg' \" />"
    return thumbnail

def deleteThumbnails():
    bucket = boto3.resource('s3').Bucket(bucketname)
    for key in bucket.objects.filter(Prefix="thumbnail/"):
        if not key.__eq__(boto3.resource('s3').ObjectSummary(bucketname, unicode("thumbnail/dummy.jpg"))):
            key.delete()
    for key in bucket.objects.filter(Prefix="src/"):
        if not key.__eq__(boto3.resource('s3').ObjectSummary(bucketname, unicode("src/dummy.jpg"))):
            key.delete()