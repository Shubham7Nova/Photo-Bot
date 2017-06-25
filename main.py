from keys import ACCESS_TOKEN
#Requests imported for using GET/POST and Json.
import requests
#Urllib imported for downloading images.
import urllib
#Textblob imported for Natural Language Processing(Deleting negative comments.)
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

BASE_URL = "https://api.instagram.com/v1/"

#Defining likes_count for storing id of posts with minimum or maximum
likes_count = {}

#Defining function for prinitng our own info.

def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_TOKEN)
    print "GET request URL for self info : %s." % (request_url)
    #Syntax for using GET and JSON Parser(Will be the same for every GET request).
    user_info = requests.get(request_url).json()
    print user_info
    if user_info['meta']['code'] == 200:
        if len(user_info["data"]):
           #printing details from user_info dictionary(Similar syntax for all JSON GET requests).
            print "Username: %s." % (user_info['data']['username'])
            print "Number of followers: %s." %(user_info['data']['counts']['followed_by'])
            print "Following: %s." % (user_info['data']['counts']['follows'])
            print "Number of posts: %s." % (user_info['data']['counts']['follows'])
        else:
            print "User does not exist."
    else:
        print "Status code other than 200 received."


#Function for getting user id of any user.

def get_user_id(insta_username):
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s") % (insta_username,ACCESS_TOKEN)
    print "Request URL for User ID : %s" % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print "Status code other than 200 received"
    exit()

#Function for getting recent information about a user using User ID.

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "Invalid Username."
        exit()
    request_url = (BASE_URL + "users/%s/?access_token=%s") % (user_id,ACCESS_TOKEN)
    print 'GET request url for info of a user: %s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

#Function for getting our own posts.

def get_own_post():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (ACCESS_TOKEN)
    print ("GET request URL for getting own posts: %s") % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if (own_media['data']):
            #Saving image name as image ID.
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media ['data'][0]['images']['standard_resolution']['url']
            #code for downloading the selected image.
            urllib.urlretrieve(image_url,image_name)
            print "Your image has been downloaded."
        else:
            print "Post does not exist!"
    else:
        print "Status code other than 200 received."

def num_of_likes(insta_username):
    user_id = get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            #Declaring dictionaries which will be copies of the dictionary of images with max and min likes respectively.
            likes_count["min_id"] = 0
            likes_count["max_id"] = 0
            #Declaring dictionaries which will hold the value of number of likes.
            likes_count['min'] = 0
            likes_count['max'] = 0
            #Condition for getting images with max and min number of likes.
            for x in range(0, len(user_media['data'])):
                if likes_count["min"] > user_media['data'][x]['likes']['count']:
                    likes_count['min_id'] = x
                    likes_count['min'] = user_media['data'][x]['likes']['count']
                if likes_count['max'] < user_media['data'][x]['likes']['count']:
                    likes_count['max_id'] = x
                    likes_count['max'] = user_media['data'][x]['likes']['count']

#Function for getting posts of a user.

def get_user_post(insta_username):
    # getting user id from username.
    user_id = get_user_id(insta_username)
    if user_id is None:
        print "User doesn't exist"
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'Requestig url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            i = None
            num_of_likes(insta_username)
            print "Select criteria for selecting post : "
            print "1) Minimum Likes.\n2) Maximum Likes."
            post_choice = int(raw_input("Please Enter Your Post Selection Criteria : "))
            while post_choice != 1 or 2 or 3:
                if post_choice == 1:
                    i = likes_count['min_id']
                elif post_choice == 2:
                    i = likes_count['max_id']
                elif post_choice == 3:
                    i = 0
            # getting image information from user_media
            image_name = user_media['data'][i]['id'] + ".jpeg"
            img_url = user_media['data'][i]['images']['standard_resolution']['url']
            # downloading the image using its url and saving it with img_name.
            urllib.urlretrieve(img_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "Post doesn't exist."
    else:
        print "Status code other than 200 received. [%d]" % user_media['meta']['code']

#Function to get Media ID of the recent posts by a user.

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User does not exist."
        exit()
    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") % (user_id,ACCESS_TOKEN)
    print ("GET request URL for getting post ID: %s") % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print "There is no recent post."
            exit()
    else:
        print"Status code other than 200 received."

#Function declaration to get the list of people who have liked the recent post of a user.

def get_like_list(insta_username):
    media_id  = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_id,ACCESS_TOKEN)
    print ("GET request URL for getting like list: %s") % (request_url)
    likes_info = requests.get(request_url).json()

    if likes_info['meta']['code'] == 200:
        if len(likes_info['data']):
            # Condition for iterating in the likes info dictionary for printing the list of likes.
            for x in range(0, len(likes_info['data'])):
                print likes_info['data'][x]['username']
        else:
            print "No user has liked the post yet!"
    else:
        print "Status code other than 200 received!"

#Function to like the post of a user.

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes") % (media_id)
    #Declaring payload dictionary for using POST.
    payload = {"access_token": ACCESS_TOKEN}
    print "POST request URL : %s" % (request_url)
    #Code for posting a like.
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print "Like was successful.!"
    else:
        print "Your like was unsuccessful. Try again!"

#Function to get list of comments on a media using media id.

def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s")%(media_id,ACCESS_TOKEN)
    print "GET request URL for getting comment list: %s" % (request_url)
    comment_list = requests.get(request_url).json()
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            #Condition for iterating in the comment_list dictionary for printing the list of comments.
            for x in range(0, len(comment_list['data'])):
                print "%s commented : %s." % (comment_list['data'][x]['from']['username'],comment_list['data'][x]['text'])
        else:
            print "There are no comments on the post."
    else:
        print "Status code other than 200 received."

#Function added for posting a comment on a post.
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("What do you want to comment?\n")
    #Payload defined for posting a comment.
    payload = {"access_token" :ACCESS_TOKEN,"text" :comment_text}
    request_url = (BASE_URL + "media/%s/comments") % (media_id)
    print 'POST request url for posting a comment : %s' % (request_url)
    make_comment = requests.post(request_url).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added your comment!"
    else:
        print "Unable to add comment. Try again!"


#Code for deleting negative comments.
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Deleting negative comments using TextBlob.
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer = NaiveBayesAnalyzer())
                #Condition for checking if the comment is positive or negative.
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id,ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

#Defining tag names for an event through which user can search for an activity/event using its tag names.
event_tags = ["tech","games"]

#Function for searching by tagnames associated with an event(subtrends).

def tag_search(insta_tagname):
    request_url = (BASE_URL + "tags/search?q=%s&access_token=%s") % (insta_tagname,ACCESS_TOKEN)
    print "GET request URL for Tag Search is : %s" % (request_url)
    activity_subtrends = requests.get(request_url).json()
    if activity_subtrends['meta']['code'] == 200:
        if len(activity_subtrends['data']):
            for x in range(0,len(activity_subtrends['data'])):
                print "Name : " + activity_subtrends['data'][x]['name']
                print ("Media count for tag is : %s") % (activity_subtrends['data'][x]['media_count'])
        else:
            print "Searched tag gave no results.!"
    else:
        print "Access code other than 200 received."


#Function for showing menu of the bot from which user can select required function via standarad input.
def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to PhotoBot for Instagram.!'
        print 'Here are the list of things you can do:'
        print "a.Get your own details.\n"
        print "b.Get details of a user by username.\n"
        print "c.Get your own recent post.\n"
        print "d.Get the recent post of a user by username.\n"
        print "e.Get a list of people who have liked the recent post of a user.\n"
        print "f.Like the recent post of a user.\n"
        print "g.Get a list of comments on the recent post of a user.\n"
        print "h.Make a comment on the recent post of a user.\n"
        print "i.Delete negative comments from the recent post of a user.\n"
        print "j.Search for an event or activity using subtrends(tag).\n"
        print "k.Exit."

        choice = raw_input("Enter you choice: ")
        #Various function calls encoded in the corresponding choices.
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)
        elif choice == "f":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice == "g":
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice == "h":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice == "i":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == "j":
            insta_tagname = raw_input("Enter the name of the tag without a leading # and without spaces. Eg.(nofilter,followorfollow)\n")
            #Condition for searching the tag only if its an official tag of the event by comparing the input tag with the official tag list of the event.
            for x in event_tags:
                if x in insta_tagname:
                    tag_search(insta_tagname)
                    break
                else:
                    print "Invalid tag searched."
        elif choice == "k":
            exit()
        else:
            print "Wrong choice. Select another option from the menu.!"

start_bot()



