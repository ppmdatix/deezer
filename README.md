### DEEZER test
The purpose of this README is to explain the analytic process and the chosen solution.

## Analytic process
First I have tried to understand the data set in order to eliminate the unuseful data.
I have concluded that the timespan and the song_id wouldn't be relevant.
Then I have looked for the extreme values that were obviously related to hacking. 
In order to have an idea on user behaviour, I have ploted som histograms.

Then I had to define the boudaries of hacking. 
I have spent some time on the Internet know how much regular peole listen to music every day.
I have considered that a song lasts an average of 3min.
And I have considered that spending more than 10 hours a day on deezer is suspicious.
As a consequence, I have settled the upper bound of regular use of Deezer at 200 songs a day.

If a user_id (or an adress_ip) occurs more than 200 times, it is considered as suspicious.
But then I have to find the purpose of the hack. So I check if it is related to the same artist_id or provider_id more than 200 times. If it is, the user_id (or the adress_id) is considered as hacked.

Then I clean the data set of all the logs related to a considerded-as-hacked user_id or adress_ip.


Finally I find the Top ten of listened artists. 
