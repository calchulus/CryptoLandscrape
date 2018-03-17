

# CryptoLandscrape [(Link)](https://calchulus.github.io/CryptoLandscrape)
Painting a clearer picture of the crypto world using data scraping.
## Inspiration
I've been learning Python in my CS course, and wanted to utilize my pandas & BeautifulSoup to gather some unique data on crypto projects and their github activities.

## Table of Contents
github.csv contains outdated information from Cryptomiso.com
social.py includes all of the messy code I used to gather this data
full_diustance.csv is a complete correlation matrix of all 577 projects found on Github and how similar their descriptions were.
average_distance.csv has a measure of how unique each of the project's descriptions were.
uniqueness.csv excludes coins with no data (scores of 0)

## Takeaways
- Interesting phenomena can be found in this list - some of the oldest projects in theory should have least unique descriptions because forks and other minor projects are based off of them by nature, but yet bitcoin and other projects are still one of the lowest correlation factors with other projects.
- Bitcoin forks were less unique vs. other projects than bitcoin itself.
- Meanwhile, industry focused projects might be more separate from the rest, and should score much lower, but not many reputable projects differed more from the crowd than the originals like Bitcoin and ETH Classic.

## What does this code do & What did I use?
Using Cryptomiso.com for a list of github repositories (many projects are not listed under their official name), I use Beautiful Soup to gather information from each project's github website. 
I then take in this text, and churn it through Python's Natural Language Processing Toolkit and a jaro-winkler distance function to uncover some similarity scores between different project's descriptions, 

## Challenges I ran into
Of course, this data wasn't in a neat dataset, so for many coins there is incomplete information, leaving simply zeros for many of these projects. However, part of this project also uncovered the extent to which many crypto projects do not have true open source availability to their projects - less than 37% of projects were found to even have a GitHub page, let alone have significant activity on it.

## Accomplishments that I'm proud of
Getting around some rate limiting and other errors with GitHub's repo design (loading taking longer than the Beautiful Soup & the requests.get() call)
Finding out how many things were bitcoin forks (answer: too many)

## What I learned
I was able to uncover some really neat data on project activity to understand how open-source some of these projects are, as well as how similar some of these projects might be.

## What's next for CryptoLandscrape
I'm working on extending this cloud of crypto project descriptions to better map out the connections between different projects, such that individuals can better know all of the projects within a specific genre/industry focus, etc.

I've also been working on gathering some alternative text sources like reddit threads and other discussion posts to understand what % of these project's communities are investors or developers (who may be using more technical language to discuss the project).
