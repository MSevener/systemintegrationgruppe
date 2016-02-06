import boto3
import urllib2

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
    imagePath = alternativePath
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

def getThumbnailPath(key):
    imageStream = ""
    thumbnailAvailable = 0
    dummyPath = "https://s3.amazonaws.com/" + bucketname + "/thumbnail/dummy.jpg"
    path = dummyPath
    bucketkey = "thumbnail/" + key + ".jpg"
    try:
        imageStream = s3.get_object(Bucket=bucketname,Key = bucketkey)
        path = "https://s3.amazonaws.com/" + bucketname + "/thumbnail/" + key + ".jpg"
        thumbnailAvailable = 1
    except Exception as e:
        print "Nimm dummy Pfad"
    if thumbnailAvailable == 0:
        try:
            imageStream = s3.get_object(Bucket=bucketname,Key =dummy)
            path = dummyPath
        except Exception as e:
            print e
    print path
    return path
