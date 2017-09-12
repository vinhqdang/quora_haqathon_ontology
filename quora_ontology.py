#!/usr/bin/python

def flip_dictionary (old_dict):
	'''
	flip a dictionary: keys to values and values to keys
	same keys will become a list
	'''
	return dict([(value, [key for key,v in old_dict.items() if v==value]) for value in set(old_dict.values())])

def generate_ontology(input_string):
	'''
	generate the ontology
	return a dictionary with key as a parent node and values is the list of child nodes
	'''
	hierarchy = {}
	stack = []
	tree_list = input_string.split(" ")
	for i in range(len(tree_list)):
		if tree_list[i] == '(':
			stack.append(tree_list[i - 1])
		elif tree_list[i] == ')':
			stack.pop()
		else:
			if stack:
				hierarchy[tree_list[i]] = stack[len(stack) - 1]
	return (flip_dictionary(hierarchy))

def load_questions(question, question_database):
	'''
	parse a question (topic + content) and add to the database
	the database in a dictionary that includes keys (topic) and values (list of questions)
	return the updated database
	'''
	(topic, question_content) = question.split(': ', 1)
	if topic in question_database.keys ():
		question_database[topic].append (question_content)
	else:
		question_database[topic] = [question_content]
	return question_database

def answer_query(query, ontology, question_database):
	'''
	answer an query
	using BFS to travel through all child topics
	'''
	query_topic, query_content = query.strip().split(' ', 1)
	topics = [query_topic]
	
	count = 0
	while len (topics) > 0:
		# add child topics into the list
		if topics[0] in ontology.keys():
			topics.extend(ontology[topics[0]])
		
		# process the first topic
		if topics[0] in question_database.keys():
			cur_topic = topics[0]
			N = len(question_database[cur_topic])
			for i in xrange (N):
				question = question_database[cur_topic][i]
				_index = question.find (query_content)
				if _index == 0:		# find the query content in the beginning of the question
					count += 1
			
		# remove the first topic
		topics.pop(0)
	return count
		
def main():
	N = int(raw_input())
	
	# generate the ontology
	flat_tree = raw_input()
	ontology = generate_ontology (flat_tree)
	
	# reading questions
	M = int(raw_input())
	question_database = {}
	for i in xrange (M):
		question = raw_input()
		question_database = load_questions(question, question_database)
	
	# answer query
	K = int(raw_input())
	for i in xrange (K):
		query = raw_input()
		answer = answer_query (query, ontology = ontology, question_database = question_database)
		print (answer)
		
if __name__=="__main__":
	main()