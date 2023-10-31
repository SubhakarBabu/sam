from flask import Flask, render_template, request, jsonify,redirect, url_for
import random
import re
import pymysql  # Import the pymysql library for MySQL operations



def respond(input_text):
    patterns = [
    (r'hello|hi|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you', ["I'm just a computer program, but I'm doing well. How about you?", 'I do not have feelings, but thanks for asking.']),
    (r'what is your name', ['I am a chatbot.', 'I go by the name MuBot.']),
    (r'what can you do', ['I can give playlist that can be help to enhance your taughts, provide information, and have a conversation with you. Just ask!']),
    (r'bye|goodbye', ['Goodbye!', 'Have a great day!', 'See you later.']),
    (r'chronic|eustress|acute|stress', [f'<p>Stress is our body’s response to pressures from challenging situations in life. It can be a feeling of being overwhelmed or under pressure.</p><a href="{url_for('stress')}">Here is your playlist</a>']),
    (r'persistent depressive disorder|pdd|premenstrual dyphoric disorder|pmdd|depression', [f'<p>Anxiety is a feeling of fear, dread, and uneasiness. It might cause you to sweat, feel restless and tense, and have a rapid heartbeat. It can be a normal reaction to stress.</p><a href="{url_for('depression')}">Here is your playlist</a>']),
    (r'comorbid|ptsd|complex', [f'<p>Post-traumatic stress disorder (PTSD) is a mental health condition thats triggered by a terrifying event — either experiencing it or witnessing it. Symptoms may include flashbacks, nightmares and severe anxiety, as well as uncontrollable thoughts about the event.</p><a href="{url_for('ptsd')}">Here is your playlist</a>']),
    (r'halluciation|delusion|paranoid|psychosis', [f'<p>Psychosis refers to a collection of symptoms that affect the mind, where there has been some loss of contact with reality. During an episode of psychosis, a persons thoughts and perceptions are disrupted and they may have difficulty recognizing what is real and what is not.</p><a href="{url_for('psychosis')}">Here is your playlist</a>']),
    (r'dissociative|amnesia|depersonalisation|lonliness', [f'<p>Dissociative disorders are mental health conditions that involve experiencing a loss of connection between thoughts, memories, feelings, surroundings, behavior and identity.These conditions include escape from reality in ways that are not wanted and not healthy.</p><a href="{url_for('lonliness')}">Here is your playlist</a>']),
    (r'trauma', [f'<p>serious bodily injury (as that caused by an accident or violent act) head trauma.an abnormal psychological or behavioral state resulting from severe mental or emotional stress or injury.</p><a href="{url_for('trauma')}">Here is your playlist</a>']),
    (r'autistic|aspergers|retts|austim|autism',[f'<p>Autism spectrum disorder (ASD) is a developmental disability caused by differences in the brain. People with ASD often have problems with social communication and interaction, and restricted or repetitive behaviors or interests</p><a href="{url_for('austim')}">Here is your playlist</a>']),
    (r'social|anxiety|panic|gad',[f'<p>An anxiety disorder is a type of mental health condition. If you have an anxiety disorder, you may respond to certain things and situations with fear and dread. You may also experience physical signs of anxiety, such as a pounding heart and sweating</p><a href="{url_for('anxiety')}">Here is your playlist</a>'])
    ]
    
    for pattern, responses in patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return random.choice(responses)
    return "I'm not sure how to respond to that."
def validate_user(username, password):
        
    
    try:
        db_config = {
        "host": "sql12.freesqldatabase.com",
        "user": "sql12657598",
        "password": "huBmdjSpZH",
        "database": "sql12657598",
    }
        
        
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT * FROM login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False

    except Exception as e:
        print(f"Database error: {str(e)}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def insert_login_details(username, password,email):
    try:
        db_config = {
        "host": "sql12.freesqldatabase.com",
        "user": "sql12657598",
        "password": "huBmdjSpZH",
        "database": "sql12657598",
    }

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO LOGIN (username, password,email) VALUES (%s, %s,%s)"

        cursor.execute(insert_query, (username, password,email))

        # Commit the changes to the database
        conn.commit()

        print("Login details inserted successfully.")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Close the cursor and the database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()




app = Flask(__name__)
app.static_url_path = 'static'
@app.route('/home')
def home():
    return render_template('Home.html')
@app.route('/')
def Home():
    return render_template('Home.html')
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/lmore')
def lmore():
    return render_template('lmore.html')
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        insert_login_details(username, password,email)
        
        return "Login details inserted successfully."
    
    return render_template('Login.html')
@app.route('/Login', methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if validate_user(username, password):
            # Valid user, redirect to the home page
            return redirect(url_for('Home'))
        else:
            return "Invalid username or password. Please try again."

    return render_template('Login.html')
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']
    bot_response = respond(user_message)

    return jsonify({'bot_response': bot_response})
@app.route('/stress')
def stress():
    return render_template('stress.html')
@app.route('/depression')
def depression():
    return render_template('depression.html')
@app.route('/ptsd')
def ptsd():
    return render_template('ptsd.html')
@app.route('/psychosis')
def psychosis():
    return render_template('psychosis.html')
@app.route('/lonliness')
def lonliness():
    return render_template('lonliness.html')
@app.route('/trauma')
def trauma():
    return render_template('trauma.html')
@app.route('/austim')
def austim():
    return render_template('austim.html')
@app.route('/anxiety')
def anxiety():
    return render_template('anxiety.html')

if __name__ == '__main__':
     app.run(debug=True) 