# The Math behin Kubernetes - Introduction

In less than a decade, Kubernetes has become the most popular platform to manage containerized workload. Kubernetes is very approachable by both developer and system administrateurs thanks to its declrartive configuration synthax and the numerous tools created by the community.

While simple to use, administrating a Kubernetes cluster arraise many challenges. Challenges you learn to deal with when lurning kubernetes such as: autoscaling, sizing node, assigning request and limites, configuring probes. etc. For each of the problem it is quite easy to find tools or empirical solution. 

Quite often solutions to sizing problem you will find over the internet relies on rules of thumbs. In most of cases they make a lot of sense et provide a very good approximate solution to the problem they are trying to solve.

Bot my mathematical curriocity could not step there. I have a back ground in applied Mathematics, I previously studies Industtial engineering. The industrial world has been absessed with finding analitical solution to almost any operational problem. Belive me or not but many operational problem found in Kubernetes operation are the same as some clasical inventory management or packing problemes.

I decided to put back on my methematiten hat en look at kubernetes problem under another angle. I believ that it is good to look at a prebleme onder another pair of eyes from time to times. This will probably lead to a series of article.

In the one, I will explained to you what commun mathematical problemes you are facing when operating a Kubernetes Cluster.

## Defining a Kubernetes Cluster

