# DEEZER test
The purpose of this README is to explain the analytic process and the chosen solution.

## Process
First I have tried to understand the data set in order to eliminate the unuseful data.
I have concluded that the **timespan** and the **song_id** wouldn't be relevant for this analysis.
Then I have searched for extreme values that were obviously related to hacking. 
In order to have an idea on user behavior, I have plotted some histograms.

Then I had to define the boundaries of hacking. 
I have spent some time on the Internet to know how much regular people listen to music every day.
I have considered that a song lasts an average of _3 min_.
And I have considered that spending more than 10 hours a day on Deezer is (really) suspicious.
As a consequence, I have settled the upper bound of regular use of Deezer at 200 songs a day _(this boundary can be determined more properly)_ .

If a user\_id (or an ip\_adress) occurs more than 200 times, it is considered as suspicious.
But then I have to find the purpose of the hack. So I check if it is related to the same artist\_id or provider\_id more than 200 times. If it is, the user\_id (or the ip\adress) is considered as hacked.

Then I clean the data set of all the logs related to a considered-as-hacked user\_id or ip\adress.

_Remark : As a consequence, for a given user\_id, I am not able to separate the **clean** listens to the fraudulent ones_

Finally I find the Top 10 of listened artists. 

_Remark : As the definition of the most listened artists is not given, I have created 3 kinds of TOP 10 :_
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
Python version : **3.4.0** <sub> _(on my computer it is 3.4.0, but I am pretty sure it does not matter)_ </sub>

 - To run the code properly, the **path\_import** and the **data\_file** have to be specified in *deezer.py* (line 58-59).
 - To get the results in _.csv_ files, **export\_mode** has to be set on **True** in *deezer.py* (line 72), and **path\_export** has to be specified (line 62).
 - To see graphical information (_recommanded_), **printing\_mode** has to be set on **True** in *deezer.py* (line 70).
 
The **expected** result, if _export-mode_ is _True_, is 4 _.csv_ files.
 * _naive\_result.csv_
 * _with\_ip\_result.csv_
 * _with\_user\_id\_result.csv_
 * _with\_log\_result.csv_
 
Those files contains the different TOP 10 (the _naive_ one is based on logs).
 
Running the script last a little less than _2min_ on my computer. It is quite long but it is acceptable. Moreover it is quite complete.
 
 There is only one _python script_, which contains everything.
