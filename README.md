# DEEZER test
The purpose of this README is to explain the analytic process and the chosen solution.

## Analytic process
First I have tried to understand the data set in order to eliminate the unuseful data.
I have concluded that the **timespan** and the **song_id** wouldn't be relevant for this analysis.
Then I have looked for the extreme values that were obviously related to hacking. 
In order to have an idea on user behavior, I have plotted some histograms.

Then I had to define the boundaries of hacking. 
I have spent some time on the Internet to know how much regular people listen to music every day.
I have considered that a song lasts an average of 3min.
And I have considered that spending more than 10 hours a day on Deezer is suspicious.
As a consequence, I have settled the upper bound of regular use of Deezer at 200 songs a day_(this boundary can be determined more properly)_ .

If a user_id (or an adress_ip) occurs more than 200 times, it is considered as suspicious.
But then I have to find the purpose of the hack. So I check if it is related to the same artist_id or provider_id more than 200 times. If it is, the user_id (or the adress_id) is considered as hacked.

Then I clean the data set of all the logs related to a considered-as-hacked user_id or adress_ip.

_Remark : As a consequence, for a given user-id, I am not able to separate the **clean** listens to the fraudulent ones_

Finally I find the Top 10 of listened artists. 


_Remark : As the definition of the most listened artists is not given, I have created 3 kind of TOP 10 :_
* One simply based on logs
* One based on the user_ids having listened the artist
* One based on the adress_ips having listened the artist
_These ranking methods are different, so are their results_

## Result
The TOP 10 based on user_id is the same than the one based on adress_ip.
If we compare the TOP 10 based on logs after and before treatment, we notice big difference.

According to all the rankings, I think that the top artist were id:6605.

It may mean that the algorithm is quite successful
_Remark : It is complicated to grade the algorithm because the real answer is not known. It will be a challenge to implement Machine Learning on this topic._


## Instructions
Python version : 3.6.0

 - To run the code properly, the **path-import** and the **data-file** have to be specified in *deezer.py* (line 58-59).
 - To get the results in csv files, **export-mode** has to be set on **True** in *deezer.py* (line 72)
 - To see graphical information, **printing-mode** has to be set on **True** in *deezer.py* (line 70)
 
