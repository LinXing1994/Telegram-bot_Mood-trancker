#submission for assignment1 (G1)
#Lin Xing
#CHARMINE FOO ZHI MIN

import requests 
import json
import time

# add other import statements here if nec

##############################################################
# global variables 
##############################################################

chat_id =  # fill in your chat id here
api_token = '' # fill in your api token here 
base_url = 'https://api.telegram.org/bot{}/'.format(api_token)

joke_url = 'https://official-joke-api.appspot.com/jokes/random' #for random joke 


# add other global variables here 
sendMsg_url = '{}sendMessage'.format(base_url)
editMsg_url = '{}editMessageText'.format(base_url)
sendPhoto_url = '{}sendPhoto'.format(base_url)
sendDocument_url = '{}sendDocument'.format(base_url)
getUpdates_url = '{}getupdates'.format(base_url)

interval_sec=10 #get 10 seconds cooling time for function mood_tracker to ask for mood
response_time=3 #set 3 seconds for function start to wait for user's response


##############################################################
# mood_tracker 
##############################################################

def start(chat_id,response_time):

	params= {"chat_id":chat_id, "text" : 'Welcome to mood tracker, do you want to start mood tracker? \n Reply |yes| to start or anything to quit\
	\n*please reply within five seconds.'}
	requests.post(sendMsg_url,params=params)
	params = {'offset': 0}
	r = requests.get(url=getUpdates_url, params=params)
	try:
		previous_id = r.json()['result'][-1]['update_id']
	except:
		previous_id = 0


	while True:
		time.sleep(response_time) #wait for 3 seconds to get user's reply
		params = {'offset': previous_id+1}
		r = requests.get(url=getUpdates_url, params=params)
		results=r.json()['result']
		for result in results:
			a=result['message']['text'].lower()
			if a =='yes':
				mood_tracker(chat_id,interval_sec)
			else:
				params= {"chat_id":chat_id, "text" : 'Thanks for using mood tracker, have a nice day'}
				requests.post(sendMsg_url,params=params)
				time.sleep(interval_sec)
				restart() #to restart mood tracker
		if len(results)==0: #restart everything in another 10 sec if user not replying anything
			time.sleep(interval_sec)
			restart()

	return


def mood_tracker(chat_id, interval_sec):

	# write your code here
	condition=1
	status=False
	params= {"chat_id":chat_id, "text" : 'welcome to mood tracker\
	please rate your current mood: 1(poor) to 5(excellent), or you can reply |quit| to exit function'}

	requests.post(sendMsg_url,params=params)
	output=[] #to create a list to calculate average mood
	params = {'offset': 0}
	r = requests.get(url=getUpdates_url, params=params)
	try:
		previous_id = r.json()['result'][-1]['update_id']
	except:
		previous_id = 0


	while condition==1:	 #change condition here, so that it can be re-started in any if condition below
		params = {'offset': previous_id+1}
		r = requests.get(url=getUpdates_url, params=params)
		print(r.json())
		results = r.json()['result']
		for result in results:  
			if len(result)>0: 	#to make sure user always give input
				text = result['message']['text']
				if text.isdigit(): 	#if user reply valid number, calculation will start
					output.append(int(text))
					if len(output)<=10:
						final=round(sum(output)/len(output),2)	 #round up answer to 2 decimal place
					elif len(output)>10:
						output.pop(0)
						final=round(sum(output)/len(output),2)
					status=True #only when status is true, then will proceed to line 82, actually line 82-98 can be written after this, to avoide using 'status'
					
				elif text.lower()=='quit': #user can reply quit to quit function, but the programme will start again after interval_sec
					requests.post(sendMsg_url,params={"chat_id":chat_id, "text" : 'Thanks for using mood tracker, have a nice day'})
					time.sleep(interval_sec)	
					restart() #still repeat mood tracker after interval_sec, after user quit the programme.

				else: #in any other situation, user must input a valid number
					requests.post(sendMsg_url,params={'chat_id':chat_id,'text':'please response with valid number'})
					condition=1 #when the condition is not met, while loop will restart, and wait for the valid input




				print(output) #check if output adds in the responser's reply correctly
				previous_id = max(previous_id, int(result['update_id']))

				if status==True:
					#get joke when user not feeling good
					joke=requests.get(joke_url)
					joke=joke.json()['setup']+'\n'+joke.json()['punchline']
					
					if len(output)>1 and output[-1]<output[-2] or len(output)==1 and output[0]<4: 
					#when first input is less than 4 or when the latest input is smaller than previous input, sent with a random joke to please them
						requests.post(sendMsg_url,params={"chat_id":chat_id,\
							"text" : 'Oh dear, hope you feel better soon!,your average mood for the last {} data points is {}! \
							\nAnd here we have a joke for you: {}'.format(len(output),final,joke)}) 
					else: 
					#in any other situation, consider user as happy
						requests.post(sendMsg_url,params={"chat_id":chat_id, \
							"text" : 'Great to know you feeling good,your average mood for the last {} data points is {}!'.format(len(output),final)}) 
					status=False 
					
					time.sleep(interval_sec)				
					params= {"chat_id":chat_id, "text" : 'please rate your current mood: 1(poor) to 5(excellent), or you can reply |quit| to exit function'}
					requests.post(sendMsg_url,params=params)

			else:
				resart()
	return 


#mood_tracker(chat_id,interval_sec)




#a function to restart mood tracker
def restart():
	start(chat_id)
	return

start(chat_id,response_time)	