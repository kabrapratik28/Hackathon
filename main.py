from flask import Flask, render_template, Response, jsonify, request, session
from flask import Markup
from camera import VideoCamera
from twitter_streaming import get_all_tweets

import time
import numpy as np
import requests
import pandas as pd
import json
import urllib2
import json

import httplib2
from dateutil import parser
from datetime import datetime, timedelta
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import Credentials
from googleapiclient.discovery import build
from apiclient import errors

app = Flask(__name__)

# Copy your credentials from the Google Developers Console
CLIENT_ID = '942390511199-8hm280333uood463f61jblfc220dlhju.apps.googleusercontent.com'
CLIENT_SECRET = 'egLSSyq-xqtl8gHz1IDSI1n8'
CLIENTSECRET_LOCATION = './client_secret.json'
REDIRECT_URI = 'postmessage'
STR_UNDEFINED = 'Undefined'
# Check https://developers.google.com/fit/rest/v1/reference/users/dataSources/datasets/get
# for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'
ORIGIN = 'http://localhost:5000'
INT_OK = 0

_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_key = '13305e387a1341aaa454534f5c8287b0'
_maxNumRetries = 10

def exchange_code(authorization_code):
    """Exchange an authorization code for OAuth 2.0 credentials.

    Args:
      authorization_code: Authorization code to exchange for OAuth 2.0
                          credentials.
    Returns:
      oauth2client.client.OAuth2Credentials instance.
    Raises:
      CodeExchangeException: an error occurred.
    """

    flow = flow_from_clientsecrets(CLIENTSECRET_LOCATION, OAUTH_SCOPE)
    flow.redirect_uri = REDIRECT_URI
    try:
        print authorization_code
        credentials = flow.step2_exchange(authorization_code)
        return credentials
    except FlowExchangeError, error:
        logging.error('An error occurred: %s', error)
        raise CodeExchangeException(None)

def get_user_info(credentials):
    """Send a request to the UserInfo API to retrieve the user's information.

    Args:
      credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                   request.
    Returns:
      User information as a dict.
    """
    user_info_service = build(
        serviceName='oauth2', version='v2',
        http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except errors.HttpError, e:
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        return user_info
    else:
        raise NoUserIdException()

def get_authorization_url(email_address, state):
    """Retrieve the authorization URL.

    Args:
      email_address: User's e-mail address.
      state: State for the authorization URL.
    Returns:
      Authorization URL to redirect the user to.
    """
    flow = flow_from_clientsecrets(CLIENTSECRET_LOCATION, OAUTH_SCOPE)
    flow.params['access_type'] = 'offline'
    flow.params['approval_prompt'] = 'force'
    flow.params['user_id'] = email_address
    flow.params['state'] = state
    flow.params['origin'] = ORIGIN
    return flow.step1_get_authorize_url(REDIRECT_URI)


def get_credentials(authorization_code, state=None):
    """Retrieve credentials using the provided authorization code.

    This function exchanges the authorization code for an access token and queries
    the UserInfo API to retrieve the user's e-mail address.
    If a refresh token has been retrieved along with an access token, it is stored
    in the application database using the user's e-mail address as key.
    If no refresh token has been retrieved, the function checks in the application
    database for one and returns it if found or raises a NoRefreshTokenException
    with the authorization URL to redirect the user to.

    Args:
      authorization_code: Authorization code to use to retrieve an access token.
      state: State to set to the authorization URL in case of error.
    Returns:
      oauth2client.client.OAuth2Credentials instance containing an access and
      refresh token.
    Raises:
      CodeExchangeError: Could not exchange the authorization code.
      NoRefreshTokenException: No refresh token could be retrieved from the
                               available sources.
    """
    email_address = ''
    try:
        credentials = exchange_code(authorization_code)
        user_info = get_user_info(credentials)
        user_id = user_info.get('id')
        return user_id, INT_OK
        '''
        if credentials.refresh_token is not None:
            store_credentials(user_id, credentials, user_info)
            return user_id, INT_OK
        else:
            credentials = get_stored_credentials(user_id)
            if credentials and credentials.refresh_token is not None:
                return user_id,INT_OK
        '''
    except CodeExchangeException, error:
        logging.error('An error occurred during code exchange.')
        # Drive apps should try to retrieve the user and credentials for the current
        # session.
        # If none is available, redirect the user to the authorization URL.
        error.authorization_url = get_authorization_url(email_address, state)
        raise error
    except NoUserIdException:
        logging.error('No user ID could be retrieved.')
    # No refresh token has been retrieved.
    authorization_url = get_authorization_url(email_address, state)
    raise NoRefreshTokenException(authorization_url)

def respond_json(status_code, **kw):
    myjson = kw
    if status_code == INT_OK:
        myjson['status'] = 'ok'
        myjson['code'] = status_code
        return jsonify(myjson)

def connect_proc(fields=None, client_ip=STR_UNDEFINED):
    user_id, auth_status_code = get_credentials(fields['authcode'])
    return respond_json(auth_status_code), user_id

def processRequest(json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result


def result_extractor(result):
    if len(result) == 0:
        return None
    else:
        return result[0][u'scores']


def avg_data_frame(old_dict, count_old, user_curr_res):
    for i in old_dict:
        old_dict[i] = ((old_dict[i] * count_old) + user_curr_res[i]) / (count_old + 1.0)
    return old_dict

def gen(camera):
    success, image  = camera.get_frame()
    return image

def get_all_twi():
    # Azure portal URL.
    base_url = 'https://westus.api.cognitive.microsoft.com/'
    # Your account key goes here.
    account_key = '9beccad39f3d42b2b7a2aec48e724f52'
    
    headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
    
    #variables that contain user credentials to access the Twitter API
    access_key = '3503362290-vJqr2AmMqZLfIIemvpCk6Tvj2bfFze99fxYvMf8'
    access_secret = '5VE0naJPQi48M8J2ETd2zRXksfujI8EyQtTVsFqC0DCVn'
    consumer_key = 'qG3qDulRMJLi3uhehHtqRnx5I'
    consumer_secret = 'F96GON8vjUYCdTBtllQTYWUe2jl8s1UWx6r4enKs9KPLUZUIiD'

    outtweets = get_all_tweets("elonmusk",10)
    # Detect sentiment.
    batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
    i = 0
    input_texts_dict = '{"documents":['
    for tweet in outtweets:
        input_texts_dict += '{"id":"' + str(i) + '", "text":"' + tweet + '"}'
        if i < len(outtweets)-1:
            input_texts_dict += ','
        #input_texts_dict["documents"].append({"id":str(i), "text":tweet})
        i += 1
    req = urllib2.Request(batch_sentiment_url, str(input_texts_dict), headers) 
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)
    sentiment_values = []
    for sentiment_analysis in obj['documents']:
       sentiment_values.append(sentiment_analysis['score'])
    return (outtweets, sentiment_values)

def count_sentiment(sentiment_values):
    pos = 10
    neg = 10
    for each_sen in sentiment_values:
        if each_sen>=0.75:
            pos=pos+1
        else:
            neg=neg+1
    return {"positive":float(pos),"negative":float(neg)}

@app.route('/')
@app.route('/index')
def signin():
    return render_template('index1.html')

@app.route('/connect', methods=['POST'])
def app_connect():
    '''
    This API authenticates the user
    :return:
    '''
    auth_fields = json.loads(request.data)
    return_data, user_id = connect_proc(auth_fields, request.remote_addr)
    session['userId'] = user_id
    return return_data


@app.route('/video_feed')
def video_feed():
    print gen(VideoCamera())
    #return Response(gen(VideoCamera()),
    #                mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(str(np.random.rand(2,1)))

@app.route('/event_stream')
def stream():
    def event_stream():
        while True:
            time.sleep(5)
            frame  = gen(VideoCamera())

            headers = dict()
            headers['Ocp-Apim-Subscription-Key'] = _key
            headers['Content-Type'] = 'application/octet-stream'

            json_data = None
            params = None
            result = processRequest(json_data, frame, headers, params)
            ans = {}
            ans['scores'] = result_extractor(result)
            outtweets, sentiment_values = get_all_twi()
            ans['sentiment_details'] = count_sentiment(sentiment_values)
            ans['tweets'] = outtweets

            with open("/Library/WebServer/Documents/emotion.json","w") as fp:
                fp.write(json.dumps(ans))
            
            yield json.dumps(ans)

    return Response(event_stream(), mimetype="text/event-stream")
    #return render_template('line-chart-with-date-time-axis.html',data=next(event_stream()), mimetype="text/event-stream")

@app.route('/error')
def error():
    return render_template('error.html', error='Could not authenticate')

if __name__ == '__main__':
    app.secret_key = 'MY_SECRET_KEY'
    app.run(host='localhost', debug=False)