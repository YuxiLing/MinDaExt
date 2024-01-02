#! pip install openai

import openai
import os
import csv
import time
import re

API_KEY = 'change_to_your_api_key'

openai.api_key = API_KEY
model_id='gpt-4'
TABLE_PATH = './table'
TEXT_PATH = './html_text'
MAX_TEXT_LENGTH = 1800

QUESTION_PART = 'Please tell whether the following 12 data types are likely to be collected by the extension based on the description text.' + \
				'Only answer with "Yes" or "No" for each data type?' + \
				'(1) user profile information (2) health information (3) financial and payment information' + \
				'(4) authentication information (5) personal communication information ' + \
				'(6) location Information (7) web history information (8) user activity information' + \
				'(9) website content information (10) device information (11) privacy-related settings' + \
				'(12) file system? ' + \
				'Only answer with "Yes" or "No" for each data type. Only one data type is collected in maximum. Only one "yes" in your answer in maximum'


def generate_question_text(desc_text):
	question_format = 'Please read the following description text of an browser extension:'
	questions = []
	question=""

	no_of_words = len(re.split(' |\n', desc_text))
	length=0
	if no_of_words > MAX_TEXT_LENGTH:
		print("decs text is too long")
	else:
		question = question_format + '"'+desc_text+'".'+QUESTION_PART
		questions.append(question)

	return question

def generate_question_table(key, path_to_table):
	f = open(path_to_table, 'r', encoding='utf-8')
	contents = list(csv.reader(f, delimiter=','))
	#print(contents)
	fout = open('./table_formatted.txt', 'w', newline='', encoding='utf-8')
	for row in contents:
		length = len(row)
		line = ''
		for i in range(length):
			if str(row[i]) == '':
				line += '" ",'
			else:
				line += '"'+str(row[i])+'",'
		line = line[:-1]+'\n'
		fout.write(line)
	fout.close()
	fout = open('./table_formatted.txt', 'r', encoding='utf-8')
	text = fout.readlines()
	#print(text)
	sents = ''.join(line for line in text if line)
	fout.close()
	question_format = 'Please read the following data collection table:\n' #f SDK with id '+str(key)+'
	question_format += sents+QUESTION_PART
	return question_format

def process_response(response, id, desc):
	
	results = response.strip().split('\n')
	labels = [id,desc]
	
	for ans in results:
		try:
			label = ans.split(" ")[-1]
			if label == "Yes":
				label = 1
			elif label == "No":
				label = 0
			else:
				label = -1
			labels.append(label)
		except:
			labels.append(-1)
	print(response)
	f = open('./gpt_response_gpt4/'+id+'.txt', 'w', newline='')
	f.writelines(response)
	f.close()
	return labels

def ChatGPT_conversation(conversation):
	print(conversation[0]['content'])
	#print(len(conversation[0]['content']))
	'''
	response = openai.ChatCompletion.create(
		model = model_id,
		messages = conversation
	)
	'''
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt=conversation[0]['content'], #"NUS is a university that",
		temperature=0,
		max_tokens=300)
	
	return response


if __name__ == '__main__':
	# des_csv='./chrome_desc_Oct_2023.csv'
	corpus_csv='./corpus.csv'
	header = ['id', 'desc','UPI','HI','FPI','AI','PCI','LI','WHI','UAI','WCI','DI','PS','FS']
	save_results = open('gpt_results_one_label_gpt4.csv', 'a', newline='')
	writer = csv.writer(save_results, delimiter=',')
	writer.writerow(header)

	re_f = open(corpus_csv, 'r')
	content = list(csv.reader(re_f, delimiter=','))
	count=0
	for row in content:
		count+=1
		# if count>5:
		# 	break
		if row[0]=='id' or row[0]=='ID':
			continue
		id=row[0]
		desc_text=row[2]
		content = generate_question_text(desc_text)

		conversation = []
		conversation.append({'role': 'user', 'content': content})

		response = ChatGPT_conversation(conversation)
		response = response.choices[0].text #message.content
		labels=process_response(response, id, content)
		writer.writerow(labels)
			