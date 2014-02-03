# exif_sort[January 2012] / martin gehrke [martin AT teamgehrke.com]
# sorts jpg/jpegs into date folders based on exif data

from PIL import Image
from PIL.ExifTags import TAGS
import sys, os, glob

import datetime
def modification_date(filename):
    t = os.path.getmtime(filename)
    return str(datetime.datetime.fromtimestamp(t))

def get_exif(fn):
#see <a href="http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/">http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/</a>
    ret = {}
    i = Image.open(fn)
    try:
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret
    except Exception, e:
        print 'Picture ', fn, ' has no tag, error is: ', e
        return {}
    #print ret

def getexif_modification_date(filename, tag='EXIF DateTimeOriginal'):
    from SimpleCV import EXIF
    f = open(filename, 'rb')
    return EXIF.process_file(f, stop_tag=tag)[tag].printable

def format_dateTime(UNFORMATTED):
    DATE, TIME = UNFORMATTED.split()
    return DATE[2:].replace('-','').replace(':','') + '-' + TIME.replace(':','') + '-'

def get_movie_creation_date(fn):
    for line in os.popen('ffprobe -loglevel quiet -show_entries stream_tags=creation_time -i ' + fn).readlines():
        #print line
        if line[:18] == 'TAG:creation_time=':
            datetime = line[18:]
            return format_dateTime(datetime)
    return ''

def sortPhotos(path):
    EXTENSIONS_pict =['jpg','jpeg', 'png']
    EXTENSIONS_movie =['mp4', 'mov']
    EXTENSIONS = []
    for EXTENSIONS_ in [EXTENSIONS_pict, EXTENSIONS_movie]:
        [EXTENSIONS.append(ext) for ext in EXTENSIONS_]
        [EXTENSIONS.append(ext.upper()) for ext in EXTENSIONS_]
    print 'DEBUG extensions = ', EXTENSIONS
    for root, dirs, files in os.walk(path):
        if not(root[-9:]=='.@__thumb'):
            PHOTOS = []
            for EXTENSION in EXTENSIONS:
                PHOTO = glob.glob(os.path.join(root, '*%s' % EXTENSION))
                PHOTOS.extend(PHOTO)

            for PHOTO in PHOTOS:
                # first process movies
                if PHOTO.split('.')[-1].lower() in EXTENSIONS_movie:
                    DATETIME = get_movie_creation_date(PHOTO)
                    if DATETIME == '':
                        DATETIME = format_dateTime(modification_date(PHOTO))
                elif not( get_exif(PHOTO) == {}):
                    try: # trying first with SimpleCV
                        DATETIME = format_dateTime(getexif_modification_date(PHOTO))
                    except:
                        try: # trying with PIL
                            DATETIME = format_dateTime(get_exif(PHOTO)['DateTimeOriginal'])
                        except:
                            try: # trying out another tag
                                DATETIME = format_dateTime(get_exif(PHOTO)['DateTime'])
                            except: # yet another one
                                try:
                                    DATETIME = format_dateTime(get_exif(PHOTO)['DateTimeModified'])
                                except: # Giving up :-)
                                    DATETIME = '' #format_dateTime(modification_date(PHOTO))
                FILE = os.path.split(PHOTO)[-1]
                newname = os.path.join(root, "%s%s" % (DATETIME, FILE))
                #newname = os.path.join(root, "%s-%s" % (DATETIME, FILE[14:]))
                #newname = os.path.join(root, FILE[14:])
                if not(DATETIME == FILE[:14]):
                    print 'renaming ',  PHOTO, ' to ', newname
                    os.rename(PHOTO, newname)
                else:
                    pass
                    print 'already renamed ',  PHOTO, ' with date ', DATETIME
                    #os.rename(PHOTO, PHOTO.replace(DATETIME+'-'+DATETIME,DATETIME))

if __name__=="__main__":
    try:
        PATH = sys.argv[1]
    except:
        PATH = ''
    if PATH == '': PATH = os.getcwd()
    print 'Processing pictures in folder', PATH
    sortPhotos(PATH)