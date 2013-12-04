#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

                         _           _
                        | |_ ___ ___| |_ _ _ ___
                        | . | .'|  _| '_| | | . |
                        |___|__,|___|_,_|___|  _|
                                            |_|
                                    by Gaurav Deshmukh     <gauravdeshmukh42@gmail.com >

Keywords: python, tools, algorithms, codechef

Copyright (C) 2013-2014 Suttit Tech Ltd.


Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of the Secret Labs AB nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
# Dependencies:
# mechanize => http://pypi.python.org/pypi/mechanize/0.1.7b
# BeautifulSoup => https://pypi.python.org/pypi/beautifulsoup4
# html2text => https://pypi.python.org/pypi/html2text

import os
import re
import sys
import glob
import getpass
import optparse
import cookielib
import mechanize

try:
    from mechanize import Browser
except ImportError:
    print "mechanize required but missing"
    sys.exit(1)
    
try:
    from BeautifulSoup import BeautifulSoup
except:
    print "BeautifulSoup required but missing"
    sys.exit(1)
    
try:
    import html2text
except:
    print "html2text required but missing"
    sys.exit(1)

extns = {'C++':'cpp','C':'c','Java':'java'}
    
def getext(str):
    key = str.split(' ')[3].split('(')[1]
    return extns[key]

def getSolutions ():
    global br, username

    # Browser
    br = Browser()
    
    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)
    br.set_handle_robots(False)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    response = br.open("http://www.codechef.com/users/"+username)
    #print response.read()
    print len(list(br.links(url_regex=","+username)))
    for l in br.links(url_regex=","+username):
        #print l.url
        r = br.open("http://www.codechef.com"+l.url)
        
        br.open("http://www.codechef.com"+l.url)
        ln = list(br.links(url_regex="/viewsolution/"))[0]
        
        #print "http://www.codechef.com"+ln.url    
        r = br.open("http://www.codechef.com"+ln.url)

        html = ""
        for i in xrange(211):
            r.readline()
        html = html+r.readline()
        
        soup=BeautifulSoup(html)
        links=soup.findAll('a')
        for link in links:
            tmp = str(link)
            tmp2 =  str(link.contents[0])
            html = html.replace(tmp,tmp2)
        
        code = html2text.html2text(html)
        lines = code.split('\n')
        
        code = ""
        ext = getext(lines[0])

        lines.pop(0)
        comment = lines[0].split('.',1)[1]

        filename = comment.split(',')[1].split(' ')[2]+'.'+ext
        lines.pop(0)
        lines.pop(0)
        
        for line in lines:
            if '.' in line:
                words = line.split('.',1)
                if '&nbsp_place_holder;' in words[1]:
                    code = code + '\n'
                else:
                    code = code + words[1] + '\n'
            
        fp = open(filename, "w")
        fp.write (code)
        fp.close()
        print "Downloaded file "+filename
        
if __name__=="__main__":
    print "Download  codes from Codechef"   
    print "Enter username:",
    username = raw_input()
    getSolutions()
    print "Done :)"
