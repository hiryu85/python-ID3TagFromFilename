#! /usr/bin/python
from sys import argv, exit
from glob import glob
from re import match 
from string import Template
try:
    import eyeD3
except ImportError:
    print 'This script require eyeD3 Python\'s module...', 'Download and install it from http://eyed3.nicfit.net/'
    exit(0)
    
    
ID3TagMap = {
    'track' : '(?P<trackNum>\d+)',
    'title' : '(?P<title>.+)',
    'year' : '(?P<year>\d{4})',
    'artist' : '(?P<artist>.+)',
    'album' : '(?P<album>.+)',
}

if __name__ == '__main__':
    
    if len(argv) < 2:
        print 'Usage: %s "pattern" <template>' % argv[0]
        exit(1)

    file_pattern, file_template = argv[1:] 
    print 'Matching %s:' % file_pattern
          
    for fname in glob(file_pattern):
        ftitle = ''.join( fname.rsplit('.', 1)[:-1] )
        print fname+'...',
        try:
            id3tag_regex_pattern = r'^%s$' % Template(file_template).substitute(ID3TagMap)
            try:
                id3tags = match(id3tag_regex_pattern, ftitle).groupdict([])
                obj_eyeD3_tag = eyeD3.Tag()
                if not obj_eyeD3_tag.link(fname):
                    break
                obj_eyeD3_tag.header.setVersion(eyeD3.ID3_V2_3)
                for tag in id3tags.keys():
                    key = '%s%s' % (tag[0].upper(), tag[1:])
                    value = id3tags[tag].title()
                    getattr(obj_eyeD3_tag, 'set%s' % key)(value)
                
                obj_eyeD3_tag.update()
                print ' [OK]' 
            except Exception as e:
                print repr(e)
                pass
                
        except ValueError:
            pass
