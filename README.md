### DownloadAll.py


***Description:***
This Python (v3.6) downloads the HTML markup from the specified URL ("parent page") and all URLs it links to. HTML <body> content from each URL is appended to a single file (default: download.html), saved as separate HTML files, or saved a separate PDF files, in the current directory in the order the links appear in the parent page. No "a href" links contained in the resulting file are altered, so only anchor links will work in the HTML or PDF files (in a combined HTML file, duplicate anchor names could be problematic). All other relative links will be dead. Absolute URL links should still be live.

***Intent:***
DownloadAll.py is one of several tools for downloading and processing multipage HTML documents for either printout and/or loading onto a tablet reader. This follows the UNIX/LINUX philosophy of creating and using small single-purpose applications instead of large catchall ones. The entire collection of these tools is intended for personal "fair use" of online materials and must not be used for other purposes.

***Usage:***

  	DownloadAll.py [-h] [-o [OUTFILE]] [-s] [-p] url2open [sitepath]

  	Downloads all the pages from the links at the entered URL ("parent page").
  	Pages are saved as either HTML or PDF files in the directory/folder in which
  	DownloadAll is invoked. Filenames are derived from the source HTML page names
  	(http://.../filename.html). Files by the same name in the current directory
  	will be overwritten.

	positional arguments:

  	url2open            Enter the full URL of the parent page
	
  	sitepath            Optional. If omitted, the site url path of the parent
                        page will be appended to relative links

	optional arguments:
	
  	-h, --help          show this help message and exit
  
  	-o [OUTFILE], --outfile [OUTFILE]
  
                        Optional output file name (default is download.html).
                        Usage: --outfile=filename
						
  	-s, --separate      Optional flag. If present, pages are saved to separate
                        files instead of appended to one combined one. File
                        names are taken from each downloaded page
                        (http://.../filename.html).
						
  	-p, --pdf           Optional flag. If present, pages are saved as separate
                        PDF files (http://.../filename.html saved as
                        filename.pdf). The -o and -s options have no effect
                        when -p is used. Since external programs exist to
                        combine pdf files, there is no option here to save a
                        combined PDF file.

