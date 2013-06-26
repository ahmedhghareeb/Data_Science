
## The Million Song Dataset Challenge

####*Objective/Abstract:*
**What is the paper about, and what was the goal of the paper?**

The goal of the paper was to explain a challenge and give the background behind it. The challenge was to predict the songs that a user will listen to, given both the user's listening history and meta-data for all songs. The paper also explained the taste profile data, the goals and design choices in creating the challenge, and presented baseline results using simple, off-the-shelf recommendation algorithms.

Academic research in this area had previously been poor for a number of reasons:

* The lack of publicly available, open and transparent data for personalized recommendation has prevented academic research on the problem.
* Privacy and intellectual property concerns typically prevent the open evaluation and publication of data which are crucial to academic study.


####*Hypothesis:*
**Where any hypothoses made within the paper before the work began? If so, what was it? What did you think about it?**

Similar Studies:

* Netflix Prize - Explicit ratings, movies
* MIREX - Audio similarity (not necessarily recommendation)
* Other small-scale, purely collaborative filtering studies

About the data:

* 1.2 million users, 380,000 songs
* No demographic or timestamp data because of privacy
* The data is open: meta-data, audio content-analysis, and standardized identifiers are available for all songs. Data was collected from several complementary data sets on same songs. The meta data includes audio features, tags on artist, tags on song, lyrics, covers, similar artists, similar songs.
* The data is large-scale, and comprised of listening histories from over one million users, providing a realistic simulation of industrial recommendation settings.

The Taste Profile Subset included:
* User ID
* Song ID
* Play count

Other things to note:

* Long-tail in popularity
	* Half have <13 unique listeners
	* 95% have < 488 unique listeners
* Collaborative filtering alone not good enough
* Based on implicit feedback (playcount), as opposed to explicit feedback (rating). Easier to gather, consistent across services

Evaluation:

Specically, for each user, the recommender observes a subset of the songs consumed by the user. It tries to produce a ranking of the songs based on this training data. Ideally, songs consumed by the user will rank higher than songs not consumed by the user. In evaluation, the exact number of times the song was consumed is not important

####*Methods:*
**What methodologies did the paper use to approach its objective? How well did they work?**

Baseline methods:

* Popularity - Song bias: Recommends songs based on popularity without taking into account user preferences.
* Same artist - Greatest hits: Most popular songs by the artists the user has already listened to. This model is maximally conservative but can work well in conjunction with other models.
* Latent factor model - BPR: Algorithm that works well for implicit feedback. Consumed items are ranked higher than no feedback items.

Same artist did the best of the 3.


####*Conclusions:*
**Overall assessment of the paper. This is generally broken into parts of what you thought about the material you read, do you think it was well written or poorly written, how well did it answer the questions it was looking at, and did you have any follow up questions about the data, methodologies, etc.**

The competition seemed to do pretty well in getting people involved since 153 teams participated in the competition.

The one question/criticism I had was around the evaluation criteria. The way the evaluation criteria was set up, it was more about accurately predicting listening history and doesn't emphasize helping with discovery. I'm not sure how you measure that in Kaggle though. In the real world, ideas to measure success could be to AB test it on Pandora or look at number of time a user hits skip.


Sources:

* [Paper](http://www2012.org/proceedings/companion/p909.pdf)
* [Kaggle Page](http://www.kaggle.com/c/msdchallenge) 
* [Paper by 3rd place team](http://cs229.stanford.edu/proj2012/NiuYinZhang-MillionSongDatasetChallenge.pdf)
