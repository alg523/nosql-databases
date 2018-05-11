# Put the use case you chose here. Then justify your database choice:
# The use case I chose was HackerNews and the database choice I went with was mongodb. I originally thought 
# I would go with neo4j as I felt the graph model would be a good way to show the relationships between post
# submissions and users but I ended up going with mongodb because I felt the document model was better suited
# so that I may take advantage of the embedded data models that are possible in mongodb
#
# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
# Even if the coffee takes out one of the servers, there should multiply copies of the data within the clusters
# on different servers (due to mongodb's replication feature)
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
# User data, votes/karma, and favorites are too important to lose as this is data that that the user needs to 
# access the app and/or data that can't easily be replaced. I am assuming that any form of posts by a user (such
# as articles, questions, and etc.) can be replaced by the user themselves. To mitigate the risk of lost data,
# we can implement write concern for every write operation in order to ensure each write is successful and 
# replicated
#

import pymongo
from pymongo import MongoClient

client = MongoClient()
database = client.hackernews
user_collection = database.user
article_collection = database.article
comment_collection = database.comment 
vote_collection = database.vote
question_collection = database.question
showhn_collection = database.showhn
job_collection = database.jobs
favorite_collection = database.favorites

# add one user to database
def create_user(username, password):
	user_collection.insert_one(
		{"username": username,
		 "password": password,
		 "karma": 0,
		}
	)

# add one article to database
def add_article(title, link, user):
	article_collection.insert_one(
		{"title": title,
		 "line": link,
		 "submitted_by": user,
		 "points": 0
		} 
	)
	
# add one point/vote to an article
def upvote_article(title, sub_user, user):
	vote_collection.insert_one(
		{"title": title,
		 "submitted_by": sub_user,
		 "upvoted_by": user
		}
	)
	article_collection.update(
		{'title' : title},
		{'$inc' : { "points" : 1 }}
	)
	user_collection.update(
		{'username' : sub_user},
		{'$inc' : { "karma" : 1 }}
	)

# add one comment on article
def comment_article(title, sub_user, user, comment):
	comment_collection.insert_one(
		{"title": title,
		 "submitted_by": sub_user,
		 "commented_by": user,
		 "comment_message": comment
		}
	)

# add favorite to article
def favorite_article(title, user):
	favorite_collection.insert_one(
		{'username': user,
		 'title': title
		}
	)

# add one question to database
def add_question(title, sub_user, content):
	question_collection.insert_one(
		{"title": title,
		 "submitted_by": sub_user,
		 "message": content
		}
	)
	
# add one ShowHN to database
def add_showhn(title, sub_user, content, link):
	showhn_collection.insert_one(
		{"title": title,
		 "submitted_by": sub_user,
		 "message": content,
		 "link": link
		}
	)

# add one job opening to database
def add_job(title, link):
	job_collection.insert_one(
		{"title": title,
		 "link": link
		}
	)



# Create at least 3 users
create_user("zebrastripes", "abc123")
create_user("bassbeatsdrums", "password123")
create_user("hackerman", "mybirthday")
create_user("henr001", "henry")
create_user("juliet_02", "databases")
create_user("jessica_is_cool", "kernel4life")

# Create 4 article
add_article("Alex and Siri revealed to be the same AI", "lameconspiracy.fake/AI", "zebrastripes")
add_article("The Blockchain is an actual chain", "lameconspiracy.fake/blockchain", "zebrastripes")
add_article("Music Apps on the rise", "coolapps.fake/article_on_music_apps", "bassbeatsdrums")
add_article("Hackers have found a way to blockchain the cloud", "hackers.fake", "hackerman") 

# Create 4 comments
comment_article("The Blockchain is an actual chain", "zebrastripes", "hackerman", "Finally, a real conspiracy")
comment_article("Music Apps on the rise", "bassbeatsdrums", "zebrastripes", "I bet this is a conspiracy")
comment_article("Hackers have found a way to blockchain the cloud", "hackerman", "hackerman", "I'm gonna try this")
comment_article("Hackers have found a way to blockchain the cloud", "hackerman", "bassbeatsdrums", "pretty cool")

# Create 4 favorites
favorite_article("Music Apps on the rise", "henr001")
favorite_article("The Blockchain is an actual chain", "henr001")
favorite_article("Alex and Siri revealed to be the same AI", "hackerman")
favorite_article("Music Apps on the rise", "zebrastripes")

# Create 1 question
add_question("Ask HN: How to create a startup", "henr001", "What's the first step to create a startup?")

# Create 1 ShowHN
add_showhn("Show HN: Javascript Business Card", "hackerman", "", "github.fake/fake")
 
# Create 1 job opening
add_job("Generic Startup is hiring", "startup.fake")



 
# Action 1: <Kevin signs up for account>
create_user("coolusername", "hunter12")

# Action 2: <Kevin publishes an article>
add_article("Blockchain and Bitcoins", "fakeurl.fake", "coolusername")

# Action 3: <Henry upvotes an article>
upvote_article("Blockchain and Bitcoins", "coolusername", "henr001")

# Action 4: <Henry comments on an article>
comment_article("Alex and Siri revealed to be the same AI", "zebrastripes", "henr001", "I knew it")

# Action 5: <Juliet favorites an article>
favorite_article("Blockchain and Bitcoins", "juliet_02")

# Action 6: <Juliet posts a question>
add_question("Ask HN: What database course should I take", "juliet_02", "I am interested in a database course. Which one should I take?")

# Action 7: <Jessica posts a ShowHN>
add_showhn("Show HN: A lightweight microkernel", "jessa_is_cool", "I made a microkernel. Check it out.", "github.fake/fakekernel")

# Action 8: <Jessica posts a job opening>
add_job("Looking for someone to maintain kernel", "kerneljob.fake")


