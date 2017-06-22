from keys import ACCESS_TOKEN
import requests
import urllib
BASE_URL = "https://api.instagram.com/v1/"

#Defining function for prinitng our own info.

def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_TOKEN)
    print "GET request URL for self info : %s." % (request_url)
    user_info = requests.get(request_url).json()
    print user_info
    if user_info['meta']['code'] == 200:
        if len(user_info["data"]):
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
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media ['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print "Your image has been downloaded."
        else:
            print "Post does not exist!"
    else:
        print "Status code other than 200 received."

#Function for getting posts of a user.

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s")%(user_id,ACCESS_TOKEN)
    print ("GET request URL for getting posts of a user: %s") % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len((user_media['data'])):
            image_name = user_media['data']['0']['id'] + ".jpeg"
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print "Your image has been downloaded."
        else:
            print"Post does not exist."
    else:
        print "Status code other than 200 received."

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
    payload = {"access_token": ACCESS_TOKEN}
    print "POST request URL : %s" % (request_url)
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
            for x in range(0, len(comment_list['data'])):
                print "%s commented : %s." % (comment_list['data'][x]['from']['username'],comment_list['data'][x]['text'])
        else:
            print "There are no comments on the post."
    else:
        print "Status code other than 200 received."
#get_comment_list("shubham7nova")






