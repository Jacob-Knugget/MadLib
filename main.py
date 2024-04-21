from flask import Flask, request, render_template, session
import random

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'SIH*v-6u)c>q<;;h&);cRw,1E_CO8>'

def create_madlib_dict(mlib_string):
  count = 0
  words = mlib_string.split() # Split string into a list of words.
  new_dict = {}
  for word in words:
    if "_" in word:
      key = word[1:word.find("/")]
      new_dict[key] = "", count
      count += 1
  return new_dict # Return the new dictionary instead of {}.

def prompt_user_for_words(mad_lib_dict):
  answers_dict = mad_lib_dict.copy() # Make an independent copy of the dictionary.
  for keys in answers_dict:
    answer = request.form['answer' + str(answers_dict[keys][1])]
    answers_dict[keys] = [answer, answers_dict[keys][1]]
  return answers_dict
  
def create_output(ml_dict, text):
  new_text = text  # Assign the starting value to new_text.
  for (key, value) in ml_dict.items():
    label = '_' + key + '/'
    new_text = new_text.replace(label, value[0])
  return new_text

def check_inputs(mad_lib_dict):
  for keys in mad_lib_dict:
    if mad_lib_dict[keys][0] == "":
      return False
    else:
      return True

@app.route('/', methods = ['GET', 'POST'])
def index():
  mad_libs = ['Suprisingly _person1/ does not find joy in _verb1/. They would rather hunt _adjective1/ vampires.',
              'In the kingdom of _place1/ a _adjective1/ _noun1/ seeks _verb1/ to _goal1/ with the help of a _creature1/.',
              'Deep in the _location1/, a _title1/ _occupation1/ discovered a _object1/ that _verb1/ with power.',
              'Within the castle walls, a _adjective1/ _noun1/ _verb1/ a _noun2/',
              'In the land of _place1/, a _title1/ _occupation1/ journeys to find the _adjective1/ _object1/ that will _verb1/ the _noun1/']
  tab_title = 'Mad Lib'
  page_title = 'Flask Game'
  if request.method == 'POST':
    user_responses = prompt_user_for_words(session['mlib_dict'])
    if check_inputs(user_responses) == True:
      output = create_output(user_responses, session['mad_lib'])
      session['still_filling'] = False
    else:
      output = "Please fill in all the blanks."
  else:
    output = ''
    session['still_filling'] = True
    session['mad_lib'] = mad_libs[random.randint(0, len(mad_libs) - 1)]
    session['mlib_dict'] = create_madlib_dict(session['mad_lib'])

  return render_template('mad_lib.html', mlib_dict = session['mlib_dict'], output = output, tab_title = tab_title, page_title = page_title)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)