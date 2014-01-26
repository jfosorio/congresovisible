
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
        to a pickle file: 
            cva.download_data() 
        '''
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
    print('The pickle file: '+filename+' has been created!')
    
   
def load_data(file='2014-01-25_candidates.p'):
    ''' Obtain the data an ad Id number to treat the columns separately when needed'''
    registers = pickle.load( open(file, 'rb' ) )
    for i in range(len(registers)):
        registers[i]['id'] = i
    return(registers)
    
def create_dataframe(registers):
    info_keys = ['id','candidate_for','first_name','last_name','gender',
    'investigations','list_number']
    candidates_df = pd.DataFrame(registers, columns=info_keys)
    parties = [] 
    trajectories  = [] 
    topics =[]
    for rec in registers:
    # The value name in party is replaced by  party_name that is more general
        party = {'id':rec['id'],'party_name':rec['party']['name']}
        trajectory = {'id':rec['id'],
        'highlighted_projects':rec['trajectory']['highlighted_projects'],
        'years_in_congress': rec['trajectory']['years_in_congress'],
        'main_topics': rec['trajectory']['main_topics'], 
        'politic_control_summonses': rec['trajectory']['politic_control_summonses']}
        topic = {'id':rec['id']}
        for topic_position in rec['topics_positions']:
            topic[topic_position['name']] = topic_position['posicion']
        parties.append(party)
        trajectories.append(trajectory)
        topics.append(topic)
    parties_df = pd.DataFrame(parties)
    trajectories_df = pd.DataFrame(trajectories)
    topics_df = pd.DataFrame(topics)
    candidates_df = pd.merge(candidates_df,parties_df)
    candidates_df = pd.merge(candidates_df,trajectories_df)
    candidates_df  = pd.merge(candidates_df,topics_df)
    return(candidates_df)
    
    
    
    