from celery import Celery
import libraryTesting
import countWords

app = Celery('tasks', broker='amqp://localhost//')

@app.task
def reverse(string):
    return string[::-1]

@app.task
def get_post_like_comment_location(graph , post):
        location = []
        amount_likes = {}
        amount_comment = {}
        postString = []

        for post in post['data']:
            likes = graph.get_object(id=post['id'], fields='likes')
            comment = graph.get_object(id=post['id'], fields='comments')
            place = graph.get_object(id=post['id'], fields='place')

            if 'message' in post:
                    print(post['message'])
                    pos, neg = libraryTesting.testing(post['message'])
                    print("positive " + str(pos))
                    print("negative " + str(neg))
                    postString.insert(0,post['message'])

            if 'place' in place :
                # location['name'] = place['place']['name']
                location.insert(0 , ( place['place']['location']['latitude'],place['place']['location']['longitude']))

            if 'likes' in likes :
                for likes in likes['likes']['data']:
                    # print likes

                    if not likes['id'] in amount_likes:
                        amount_likes[likes['id']] = 1;
                    else:
                        amount_likes[likes['id']] += 1;

            if 'comments' in comment:

                for comments in comment['comments']['data']:

                    print comments['from']['id']
                    print comments['message']
                    if not comments['from']['id'] in amount_comment:
                        amount_comment[comments['from']['id']] = 1;
                    else:
                        amount_comment[comments['from']['id']] += 1;

        if(amount_likes):
            amount_likes['top'] = max(amount_likes, key=amount_likes.get)

        if (amount_comment):
            amount_comment['top'] = max(amount_comment, key=amount_comment.get)

        print(countWords.freqDictionary(postString))
        print(location)

        return amount_likes, amount_comment, location