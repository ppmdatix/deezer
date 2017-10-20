#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Creation : 20/10/17

@author: ppx
"""
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
PURPOSE OF THE ALGORITHM :

Analyze the provided data set and produce a daily Artists Top 10 based on their listening count. 
Some of the listens in the data set could be considered fraudulent and should be deleted before computation.
"""
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
PACKAGES IMPORTED :
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# If a package is not working, run 'pip install name_of_the_package' in your terminal
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
VARIABLES :
"""
### IMPORT
path_import = '/Users/ppx/Downloads/test_fraud/'
data_file = 'listen-20131115.log'

### EXPORT
path_export = '/Users/ppx/Desktop/BP/data-science-script/exemple/result/'
result_file = 'the_result_file.csv'

### PONCTUAL 
action_made = - 1
action_number = 1
print_progress_mode = True
headers_name = ['timestamp','sng_id','user_id','artist_id','provider_id','ip']
column_type = {'timestamp': np.int64,'sng_id':np.int64,'user_id':np.int64,'artist_id':np.int64,'provider_id': np.int64,'ip':np.string_}

every = 0
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
DEFINITION OF FUNCTIONS :
"""
"""
Pour des raisons de performances, il est nécessaire de transformer les adresses ip en chaine de caractère.
Sous Python, comparer deux integer est plus rapide que de compararer des strings
"""
def turn_ip_into_integer(string):
    result = list(string)
    length = len(result)
    for k in reversed(range(0,length )):
        if result[k] == '.':
            del result[k]
        # else:
        #     result[k] = int(result[k])

    result = int("".join(result)) 
    return result
"""
"""


"""
Les trois fonctions qui suivent sont là pour vérifier l'avancement de certains calculs
"""
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def print_progress(mode):
    global action_made
    global action_number
    if mode == True:
        action_made += 1
        restart_line()
        printProgressBar(action_made, action_number, prefix = 'Progress:', suffix = 'Complete', length = 50)







def ploting_data(df, granularity = 50, print_mode = True, start_plot = 100):
    
    maxi_w = max(df)
    mini_w = min(df) + start_plot

    bins_w = np.linspace(mini_w, maxi_w, granularity)

    if print_mode:
        plt.hist(df,bins_w)
        plt.title(df.name )
        plt.show()
        plt.close()


"""
Il s'agit de la fonction qui detecte les hackers
"""
def list_fake(var = 'ip', testing_dict = every, affichage = True):
    """
    ENTREE:
        @var : string
            le nom de la variable de regroupement (user_id ou ip)

        @testing_dict : dict of lists
            la liste des entités (user_id ou ip) à tester

        @affichage boolean
            afficher oui ou non un extrait de la sortie 

    SORTIE:
        @df_ = dataframe qui resume l'activite des entités
        
    """

    global first_data, action_made, action_number ### action_made et action_number sont là pour le print_progress

    df_ = pd.DataFrame( columns=[var,'nombre_ecoute','max_artist_id','max_provider_id']) ### on crée le dataframe vide qui va receuillir les résultats

    action_number = len(testing_dict[var])
    action_made = -1
    print("")
    for line in testing_dict[var]:### pour chaque entite dans la liste des suspects
        little_data = first_data[first_data[var] == line] ### on ne garde que les logs concernant cette entité
        """
        little_data permet d'étudier les logs de l'entite vis a vis des artist_id
        """
        little_data = little_data.groupby(['artist_id']).count()
        little_data = little_data.drop(['timestamp','ip','sng_id','user_id'],1)
        little_data = little_data.rename(columns = {'provider_id': 'count'})
        """
        little_data_bis permet d'étudier les logs de l'entite vis a vis des provider_id
        """
        little_data_bis = first_data[first_data[var] == line]
        little_data_bis = little_data_bis.groupby(['provider_id']).count()
        little_data_bis = little_data_bis.drop(['timestamp','ip','sng_id','user_id'],1)
        little_data_bis = little_data_bis.rename(columns = {'artist_id': 'count'})
        col_data = [[line,len(first_data[first_data[var] == line]),max(little_data['count']),max(little_data_bis['count'])]]
        col_names = [var,'nombre_ecoute','max_artist_id','max_provider_id']
        data_inter = pd.DataFrame(col_data, columns = col_names )
        df_ = df_.append(data_inter,ignore_index=True) ### On rajoute l'analyse faite pour l'entite
        print_progress(print_progress_mode)

    col_type = {var : np.int64, 'nombre_ecoute': np.int64, 'max_artist_id': np.int64, 'max_provider_id': np.int64}
    df_ = df_.astype(dtype = col_type)
    df_ = df_.set_index(var) ### On reindexe le dataframe par les entite

    if affichage:
        df_.head()

    return df_

"""
detection_fake() prend, logiquement, en entrée la sortie de list_fake()
"""
def detection_fake(df_, print_mode = True, seuils = [50,100,200],var = 'ip'):
    """
    ENTREE:
        @df : dataframe

        @print_mode : boolean
            afficher oui ou non les graphiques "camembert"

        @seuils list of integer
            seuils de détection de sur_utilisation 

    SORTIE:
        @result = list of integer
            la liste des entités (user_id ou ip) qui sont soupçonnés de hack
    """
    for warning in seuils:
        result = []
        no_worry = 0
        no_reason = 0
        with_reason = 0
        nbr = len(df_)
        for line in df_.index:###suspect_user_id:
            if df_['nombre_ecoute'][line] < warning:
                no_worry +=1
            elif df_['max_provider_id'][line] > warning or df_['max_artist_id'][line] > warning:
                with_reason +=1
                result.append(line)
            else:
                no_reason += 1

    if print_mode:
        if not (no_worry + no_reason + with_reason == nbr):
            print('ERROR')
        else:
            print("")
            print('pas de suspicion = %s   suspicion sans raison = %s    suspicion avec raison %s' %(no_worry, no_reason, with_reason))
            labels = ['no_worry','no_reason','with_reason']
            values = [no_worry,no_reason,with_reason]
            plt.pie(values, labels = labels)###, filename='basic_pie_chart')
            plt.title(var + 'a risque avec un seuil fixé à ' + str(warning) )
            plt.show()
            plt.close()
    return result 

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
DATA READING 
"""

### on importe la data :
first_data = pd.read_csv(path_import + data_file, names = headers_name, dtype = column_type)

### On affiche la taille du dataframe, pour etre sur de la bonne importation
print('taille de la data :') 
print(first_data.shape)

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------

"""
PLAYING WITH THE DATA
"""

first_data['ip'] = first_data['ip'].apply(lambda x: turn_ip_into_integer(x)) ### transformation de l'adresse_ip en integer



### premier classement qui serait valable si le hack n'était pas présent
first_result = first_data.groupby(['artist_id']).count()[['timestamp']].rename(columns = {'timestamp':'count'}).sort_values(by = 'count',ascending = False)[:10]
first_result.plot(kind = 'bar', title = 'premier classement naif')
plt.figure()

first_data.groupby(['user_id']) ### on regroupe par user_id pour faciliter les prochains calculs
every_user_id = first_data.user_id.unique() ### on liste les user_id
every_ip = first_data.ip.unique() ### on liste les adress_ip
every = {'ip':every_ip, 'user_id':every_user_id} ### on les regroupe dans un dict



"""
On peut lancer cette partie de code afin de visualiser le nombre d'écoute par user_id
On affiche un histogramme

grouped_by_user_id = first_data['user_id'].value_counts()
grouped_by_user_id = grouped_by_user_id[grouped_by_user_id.index != 0]
ploting_data(df = grouped_by_user_id)
"""









### Une premiere detection d'user_id suspects

limite_suspecte_user_id = 200
suspect_user_id = []
for line in grouped_by_user_id.index:
    if grouped_by_user_id[line] > limite_suspecte_user_id:
        suspect_user_id.append(line)
print('il y a  %s user_id suspects' %(len(suspect_user_id)))


"""
On peut lancer cette partie de code afin de visualiser le nombre d'écoute par ip
On affiche un histogramme

first_data.groupby(['ip'])
grouped_by_ip = first_data['ip'].value_counts()
grouped_by_ip = grouped_by_ip[grouped_by_ip.index != 0]
ploting_data(df = grouped_by_ip)
"""





### Une première détection d'adresse IP suspecte
limite_suspecte_ip = 200
suspect_ip= []
for line in grouped_by_ip.index:
    if grouped_by_ip[line] > limite_suspecte_ip:
        suspect_ip.append(line)
print('il y a  %s user_id suspects' %(len(suspect_ip)))


### On regroupe les entites suspectes dans un dictionnaire
suspects = {'ip': suspect_ip, 'user_id': suspect_user_id}





### Recoupement 
### Ecoutes provenant d'adress_ip ET d'user_id suspects
ecoute_tres_suspectes = []
for line in first_data.index:
    if (first_data['user_id'][line] in suspect_user_id) and (first_data['ip'][line] in suspect_ip):
        ecoute_tres_suspectes.append(line)

pourcentage_tres_suspect = len(first_data) / len(ecoute_tres_suspectes)

print('il y a  %s pct d_ecoutes tres suspectes' %pourcentage_tres_suspect)







############
detected_suspect_user_id = detection_fake(df_ = list_fake(var = 'user_id', testing_dict = every), var = 'user_id')
detected_suspect_ip = detection_fake(df_ = list_fake(var = 'ip', testing_dict = every), var = 'ip')
############
criterion = lambda row: (row['user_id'] not in detected_suspect_user_id ) and (row['user_id'] not in detected_suspect_ip)

cleaned_data = first_data[first_data.apply(criterion, axis = 1)]


"""
df_user_id = pd.DataFrame( columns=['user_id','max_artist_id','max_provider_id'])
for user_id in every_user_id:###suspect_user_id:
    little_data = first_data[first_data.user_id == user_id]
    little_data = little_data.groupby(['artist_id']).count()
    little_data = little_data.drop(['timestamp','ip','sng_id','user_id'],1)
    little_data = little_data.rename(columns = {'provider_id': 'count'})
    little_data_bis = first_data[first_data.user_id == user_id]
    little_data_bis = little_data_bis.groupby(['provider_id']).count()
    little_data_bis = little_data_bis.drop(['timestamp','ip','sng_id','user_id'],1)
    little_data_bis = little_data_bis.rename(columns = {'artist_id': 'count'})
    col_data = [[user_id,len(first_data[first_data.user_id == user_id]),max(little_data['count']),max(little_data_bis['count'])]]
    col_names = ['user_id','nombre_ecoute','max_artist_id','max_provider_id']
    data_inter = pd.DataFrame(col_data, columns = col_names )
    df_user_id = df_user_id.append(data_inter,ignore_index=True)
col_type = {'user_id' : np.int64, 'nombre_ecoute': np.int64, 'max_artist_id': np.int64, 'max_provider_id': np.int64}
df_user_id = df_user_id.astype(dtype = col_type)
df_user_id = df_user_id.set_index('user_id')




warning = 100
for warning in [50,100,200,300]:
    no_worry = 0
    no_reason = 0
    with_reason = 0
    nbr_user_id = len(every_user_id)
    for user_id in df_user_id.index:###suspect_user_id:
        if df_user_id['nombre_ecoute'][user_id] < warning:
            no_worry +=1
        elif df_user_id['max_provider_id'][user_id] > warning or df_user_id['max_artist_id'][user_id] > warning:
            with_reason +=1
        else:
            no_reason += 1
    

    if not (no_worry + no_reason + with_reason == nbr_user_id):
        print('ERROR')
    else:
        print('pas de suspicion = %s   suspicion sans raison = %s    suspicion avec raison %s' %(no_worry, no_reason, with_reason))
    labels = ['no_worry','no_reason','with_reason']
    values = [no_worry,no_reason,with_reason]
    plt.pie(values, labels = labels)###, filename='basic_pie_chart')
    plt.show()
    plt.close()
"""



"""
warning = 100
no_worry = 0
for ip in suspect_ip:
    little_data = first_data[first_data.ip == ip]
    little_data = little_data.groupby(['artist_id']).count()
    little_data = little_data.drop(['timestamp','ip','sng_id','user_id'],1)
    little_data = little_data.rename(columns = {'provider_id': 'count'})
    little_data_bis = first_data[first_data.ip == ip]
    little_data_bis = little_data_bis.groupby(['provider_id']).count()
    little_data_bis = little_data_bis.drop(['timestamp','ip','sng_id','user_id'],1)
    little_data_bis = little_data_bis.rename(columns = {'artist_id': 'count'})
    warn = False
    if max(little_data['count']) > warning:
        print("")
        print(ip)
        print("")
        print("alerte artist_id")
        print("")
        print(little_data)
        warn = True
    if max(little_data_bis['count']) > warning:
        print("")
        print(ip)
        print("")
        print("alerte provider_id")
        print("")
        print(little_data_bis)
        warn = True
    if not warn:
        no_worry += 1
        ### print(first_data[first_data.user_id == user_id])
"""





result_by_user_id = cleaned_data.groupby('artist_id')['user_id'].nunique().sort_values(ascending = False)[:10]
result_by_user_id.rename(columns = {'user_id':'nombre d_user_id different ayant ecoute l_artiste'})
result_by_user_id.plot(kind = 'bar', title = 'TOP 10 obtenu a partir des user_id')
plt.figure()
result_by_ip = cleaned_data.groupby('artist_id')['ip'].nunique().sort_values(ascending = False)[:10]
result_by_ip.rename(columns = {'ip':'nombre d_ip differentes ayant ecoute l_artiste'})
result_by_ip.plot(kind = 'bar', title = 'TOP 10 obtenu a partir des adresses IP')
plt.figure()
result_by_log = cleaned_data.groupby('artist_id')['timestamp'].nunique().sort_values(ascending = False)[:10]
result_by_log.rename(columns = {'timestamp':'nombre de log relatifs à l_artiste'})
result_by_log.plot(kind = 'bar', title = 'TOP 10 obtenu a partir des logs')

#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
RESULT EXPORT :
"""

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
"""
CLEANING THE MEMORY
"""

del action_made
del action_number
del line
del criterion

### To run the code :
### runfile('/Users/ppx/deezer.py', wdir='/Users/ppx')

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#|
#|
#|
#|
#|
#|
#|
#|
#-------------------------------------------------------------------
#-------------------------------------------------------------------
os.system('say "fini"')
"""
END
"""

