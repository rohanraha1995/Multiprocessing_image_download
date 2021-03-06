
 #!/usr/bin/env python

import urllib
import multiprocessing
import os
import requests
import pandas as pd
########################################################################
class MultiProcDownloader(object):
    """
    Downloads urls with Python's multiprocessing module
    """

    #----------------------------------------------------------------------
    def __init__(self, urls):
        """ Initialize class with list of urls """
        self.urls = urls

    #----------------------------------------------------------------------
    def run(self):
        """
        Download the urls and waits for the processes to finish
        """
        jobs = []
	print self.urls
        for url in self.urls:

            process = multiprocessing.Process(target=self.worker, args=(url,))
            jobs.append(process)
            process.start()
        for job in jobs:
            job.join()

    #----------------------------------------------------------------------
    def worker(self, url):
        """
        The target method that the process uses to download the specified url
        """
        
	fname = os.path.basename(url)
        msg = "Starting download of %s" % fname
        print msg, multiprocessing.current_process().name
        r = requests.get(url)
        with open(fname, "wb") as f:
            f.write(r.content)

#----------------------------------------------------------------------
if __name__ == "__main__":
        fname = 'Tommy-Data.csv'
    	data = pd.read_csv(fname)
	source = data[['File_Name', 'File_Path']]
        ur=[]
	for index,row in source.iterrows():
		urls = row.File_Path
		ur.append(urls)
       	downloader = MultiProcDownloader(ur)
      	downloader.run()
