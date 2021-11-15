# AdaptiveQuiz
 Senior Project. Adaptive Quiz Web App

 # What Is It?
 A Web Based Quiz Application Basis that uses Randomization, Variation, and Score Tracking to create a unique Quiz Learning Experience

 # How to Run It (Local)
 Currently the code is configured to run only locally but has the option to be setup to run as a proper Web Page.

 To run the local code, navigate to where the source folder was downloaded inside your Command Prompt/Terminal Window and make sure you have Python installed on your machine.

 You can execute the file by doing
 ```bash
 python RebuildAdaptiveQuiz.py
 ```

 Once you do this the Web Page can be visited at http://127.0.0.1:5000/ or whatever port is edited in within the RebuildAdaptiveQuiz.py file

 # How to Run It (Hosted Web Page)
 The way to run this project as a Hosted Web Page is the same as above except the link will be different and a couple things need to be done

 Within the RebuildAdaptiveQuiz.py you will find 2 lines of code

 ```python
 app.run(debug = False, host = '10.0.0.69', port = 5000)
 app.run(debug=False, port=5000)
 ```

 The first line should be commented out with the second being active, in order to turn this application into a Hosted Web Page we will need to 
 either comment that second line out and use the first line or put a host field into the second line like the first line has.

 When doing this for either method you will need to set the Host IP Address to the IP Address the Web App will be hosted off of, and the port number you will need to open for hosting

 Lastly for this you will need to open a TCP port for hosting this Web App and when you do the address to access it should be that Host IP : Port Number like so

 ```bash
 http://10.0.0.69:5000/
 ```
 
 # Modules for Running
 All the External Code Modules used for this Project are contained within Lib.zip

 # Contact
 Feel free to contact us with any questions
 lavoiet2@wit.edu
 pantas@wit.edu
 kattels@wit.edu
 
 # How it Works
 
 # Question Sourcing
 Questions are inputted into a mysql database, and accessed through the get_questions() function onload.
 
 Types of Questions:
 -Dynamic
 -Original 
 
 Inputing Questions to the Database:
 
 Use the populateDatabaseFromCsv.py for Original Questions and csvtoDatabase.py for Dynamic Questions until the csvtoDatabase.py is updated.
 
 Questions are loaded into the questions list when the RebuildAdaptiveQuiz.py is run and holds the questions in class form, the dynamic questions are built and placed into the list aswell.
 
# Users
Users represent the players of the quiz, upon first entering the webpage http://127.0.0.1:5000/ index the user is riderected to a login page where they will signup an account that will be added to the database table users. When a user logs in flask sessioning is used to maintain access to the users class object and is easily accessed in the activeUsers dict with the players username such as activeUsers[session["data"]["username"]] (session["data"]["username"] is kept client side as a encrypted cookie)

# Question Distrubution
To be worked on...
The idea is to use a users internal score combined with the questions difficulty to adaptively change the difficulty of the questions based on users performance, there is potential for other options to distribute questions aswell.
![Probability](https://user-images.githubusercontent.com/36092187/141339596-27f1b8e6-e75a-43bb-99ed-c2113bc56e86.png)

 
 
