# Python 3.6
# =======================================
# =======================================
# DownloadAll.py
# =======================================
# ***Description***
# Downloads the HTML markup from the specified URL ("parent page") and all URLs
# it links to. HTML <body> content from each URL is appended to a single file
# (default: download.html) in the current directory in the # order the links
# appear in the parent page. No <a href> links contained in the resulting file
# are altered, so only #anchor links will work (though duplicate anchor name
# could be problematic. All other relative links will be dead. Absolute URL
# links should still be live.
# =======================================
# ***Intent***
# DownloadAll.py is one of several tools for downloading and processing multi-
# page HTML documents for either printout and/or loading onto a tablet reader.
# This follows the UNIX philosophy of creating and using small single-purpose
# applications instead of large catchall ones. The entire collection of these
# tools is intended for personal "fair use" of online materials and must not be
# used for other purposes.
# =======================================

# == Standard library ==
import argparse
import logging
logger = logging.getLogger()
import os
import re
import requests
import sys
import urllib.request
import urllib.error
# == PyPI modules/packages ==
from bs4 import BeautifulSoup
from colorama import init
init()
import pdfkit


# ================================================
# Function definitions.
# ================================================

def ask4permission():
    """Yes, I know: 'EAFP.' But I want to catch permission errors right up
    front and out in the open rather than buried in the code where the first
    instance of a file write takes place.
    """
    try:
        with open('temp.tst', 'w') as test:
            test.write('test')
    except PermissionError:
        print('\n' + '    ' + '\033[40m\033[1m\033[31m' + 'You do not have \
        permission to create files in this directory or folder')
        sys.exit()
    else:
        os.remove('temp.tst')   # If no error is raised, delete test file.
        pass


def getlinks(url, sitepath):
    """Creates a list of links from a parent-page url and all descendants.
     If a link is not a complete HTTP url, getlinks() adds a site path
    supplied as the second argument in the function call."""
    try:
        html_page = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print('\n' + '    ' + '\033[40m\033[1m\033[31m' + 'Page not found at \
            that address. Ending program. Try again.')
        sys.exit()
    except urllib.error.URLError:
        print('\n' + '    ' + '\033[40m\033[1m\033[31m' + 'Server not found at \
            that address. Ending program. Try again.')
        sys.exit()
    else:
        soup = BeautifulSoup(html_page, 'lxml')
        links = []
        fixedlinks = []
        # http = re.compile(r'http://', re.IGNORECASE)  # A 'pattern object'
        for link in soup.findAll('a', attrs={'href': re.compile('html$')}):
            links.append(link.get('href'))
        # If an element in the list (all_links) does not start with 'http' (as
        # with a site that uses relative links) then prepend site url path
        # ('http://sub.site.topdomain/dir/dir/...') and build new list. In all
        # likelyhood, most links will need prepending.
        for link in links:
            if not http.match(link):
               fixedlinks.append(sitepath + link)
        else:
            fixedlinks.append(link)
        return fixedlinks


def savefiles(linklist, outputflag):
    """Using links collected by getlinks() and parsed by bs4, this function
    saves file(s) of the html contents of the <body> tag of web pages in one
    of three ways: as separate html files, as separate PDF files (using the 
    pdfkit package and wkhtmltopdf), or by default as a single appended html
    file.
    """
    for link in linklist:
        print('\n   Getting ' + link)
        try:
            page = requests.get(link).content
        except requests.exceptions.MissingSchema:     # Non-fatal error
            print('\033[1m\033[31m' + '   URL error: ' + link + ' cannot be \
                processed' + '\033[0m')
            continue
        else:
            bsObject = BeautifulSoup(page, 'lxml')
            htmltext = bsObject.body
        try:
            if outputflag == 'html':
                seperate_file = (link.rsplit(sep='/', maxsplit=1))[1]  # Remove
                                                           # url path from link
                print('   Saving <' + seperate_file + '> in current directory')
                with open(seperate_file, 'w') as outfile:
                    outfile.write(str(htmltext))
            elif outputflag == 'pdf':
                wk_options = {'quiet':None}     # Dict for wkhtmltopdf options
                temp_link = (link.rsplit(sep='/', maxsplit=1))[1]
                pdf_file = (temp_link.rsplit(sep='.', maxsplit=1))[0] + '.pdf'
                print('   Saving <' + pdf_file + '> in current directory')
                pdfkit.from_string(
                    str(htmltext), str(pdf_file), options=wk_options)
            else:
                 with open(args.outfile, 'a') as outfile:
                     outfile.write(str(htmltext))
        except UnicodeError:                          # Non-fatal error
            print('\033[1m\033[31m' + '   Unicode codec error. One or more \
                characters may be corrupted in: ' + link + '\033[0m')
            continue


def main():
    """"Setup and handle command-line arguments and call main functions"""
    parser = argparse.ArgumentParser(
        prog='DownloadAll.py', description='''\nDownloads all the pages from 
        the Links at the entered URL ("parent page"). Pages are saved as either 
        HTML or PDF files in the directory/folder in which DownloadAll is 
        invoked. Filenames are derived from the source HTML page names 
        <http://.../filename.html>. Files by the same name in the current 
        directory will be overwritten.''')

    parser.add_argument('url2open',
        help='Enter the full URL of the parent page.')

    parser.add_argument('sitepath', default='None', nargs='?', help=
        '''Optional. If omitted, the site url path of the parent page will be 
        appended to relative links.''')

    parser.add_argument('-o', '--outfile', default='download.html', nargs='?',
        help='''Optional output file name (default is download.html). Usage: 
        --outfile=filename.''')

    parser.add_argument('-s', '--separate', action='store_true', help=
        '''Optional flag. If present, pages are saved to separate files instead 
        of appended to one combined one. File names are taken from each 
        downloaded page (<http://.../filename.html>).''')

    parser.add_argument('-p', '--pdf', action='store_true', help=
    '''Optional flag. If present, pages are saved as separate PDF files 
        (<http://.../filename.html> saved as <filename.pdf>). The -o and -s 
        options have no effect when -p is used. Since external programs exist 
        to combine pdf files, there is no option here to save a combined PDF 
        file.''')

    args = parser.parse_args()

    # Make sitepath an optional argument. If it's left off, then assume the
    # sitepath of the parent page is the correct one to use in getlinks() for
    # relative links. Create it from args.url2open.

    # Add 'http://' if user left it off the URL.    #
    http = re.compile(r'http://', re.IGNORECASE)  # Pattern-object globals
                                                  # used also in getlinks().
    https = re.compile(r'https://', re.IGNORECASE)

    if http.match(str(args.url2open)) or https.match(str(args.url2open)):
        pass
    else:
        args.url2open = 'http://' + args.url2open  # "http://" will also work in
                                                 # place of "https://" in a URL.
    if args.sitepath == 'None':
        sitepath = (args.url2open.rsplit(sep='/', maxsplit=1))[0] + '/'
    else:
        sitepath = args.sitepath

    if args.separate:
        fileflag = 'html'
    elif args.pdf:
        fileflag = 'pdf'
    else:
        fileflag = 'None'

    # Main function calls
    ask4permission()        # Check to make sure user has write permission.
                            # See the function's doc string for rationale.

    all_links = getlinks(args.url2open, sitepath)  # Since it might be derived
        # from args.url2open, args.sitepath is not referenced directly here as
        # args.url2open is.

    savefiles(all_links, fileflag)

if __name__ == '__main__':
    main()

# TODO: added logging

