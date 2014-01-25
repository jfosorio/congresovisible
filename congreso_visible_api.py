
'''
This is a library to retrive the data form congresovisible.orgs
[]

'''

import json
import urllib2
import pandas as pd
import numpy as np
import pprint as pp
import sys
import pickle
import datetime


def download_data():
    ''' This is a module to convert all the information in congresovisible
        to a pickle file'''
    # Initial URL
    url = 'http://congresovisible.org/api/apis/candidatos/'
    req= urllib2.Request(url)
    # There several URL wiht candidates everyone retrivied as response['next']
    # in the previus url
    candidates = []
    while True:
        try:
            print "Downloading URL: "+url
            response = urllib2.urlopen(req)
            data = json.load(response)
            # Concatenate the next results
            candidates+= data['results']
            url = data['next']
        except urllib2.URLError:
            print('It seems data is not available')
            sys.exit("Error message")
        if url==None:
            break
        req = urllib2.Request(url)
    today = datetime.date.today()
    filename = str(today)+"_candidates.p"
    pickle.dump(candidates, open(filename, "wb" ) )
    print('The pickle file'+filename+'has been created!)
    
   
def load_data(file='2014-01-25_candidates.p'):
    candidates = pickle.load( open(file, 'rb' ) )
    return(candidates)
    

