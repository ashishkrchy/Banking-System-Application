import random
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",  
    user="Your MySQL Username",  
    password="Your MySQL password", 
    database="quiz_app",  
)
if db.is_connected():
    print("Successfully connected to the database!")
else:
    print("Failed to connect to the database.")

cursor = db.cursor()

# Quiz questions (10 per subject)
quizzes = {
    "DSA": [
        {
            "question": "What is the time complexity of binary search?",
            "options": ["O(n)", "O(log n)", "O(n^2)"],
            "answer": "O(log n)",
        },
        {
            "question": "Which data structure is used in BFS?",
            "options": ["Stack", "Queue", "Tree"],
            "answer": "Queue",
        },
        {
            "question": "What is the worst-case time complexity of quicksort?",
            "options": ["O(n^2)", "O(n log n)", "O(n)"],
            "answer": "O(n^2)",
        },
        {
            "question": "Which of the following is not a linear data structure?",
            "options": ["Array", "Tree", "Linked List"],
            "answer": "Tree",
        },
        {
            "question": "Which data structure allows LIFO?",
            "options": ["Queue", "Stack", "Array"],
            "answer": "Stack",
        },
        {
            "question": "What is the best-case time complexity of merge sort?",
            "options": ["O(n log n)", "O(n)", "O(n^2)"],
            "answer": "O(n log n)",
        },
        {
            "question": "Which algorithm is used for shortest path in graphs?",
            "options": ["DFS", "Dijkstra", "Kruskal"],
            "answer": "Dijkstra",
        },
        {
            "question": "Which data structure is used in recursion?",
            "options": ["Stack", "Queue", "Array"],
            "answer": "Stack",
        },
        {
            "question": "What is a deque?",
            "options": ["Double-ended queue", "Double queue", "Dynamic queue"],
            "answer": "Double-ended queue",
        },
        {
            "question": "Which is a self-balancing binary search tree?",
            "options": ["AVL Tree", "B-Tree", "Binary Tree"],
            "answer": "AVL Tree",
        },
    ],
    "DBMS": [
        {
            "question": "What does SQL stand for?",
            "options": [
                "Structured Query Language",
                "Simple Query Language",
                "Standard Query Language",
            ],
            "answer": "Structured Query Language",
        },
        {
            "question": "Which of these is not a type of database?",
            "options": ["Relational", "Distributed", "Tree"],
            "answer": "Tree",
        },
        {
            "question": "Which command is used to retrieve data?",
            "options": ["INSERT", "UPDATE", "SELECT"],
            "answer": "SELECT",
        },
        {
            "question": "Which key is used to uniquely identify rows?",
            "options": ["Foreign key", "Primary key", "Candidate key"],
            "answer": "Primary key",
        },
        {
            "question": "Which is a type of JOIN?",
            "options": ["FULL JOIN", "SEMI JOIN", "PARTIAL JOIN"],
            "answer": "FULL JOIN",
        },
        {
            "question": "What is normalization?",
            "options": ["Data modeling", "Organizing data", "Data duplication"],
            "answer": "Organizing data",
        },
        {
            "question": "What is a primary key?",
            "options": ["Unique identifier", "Duplicate identifier", "Foreign key"],
            "answer": "Unique identifier",
        },
        {
            "question": "Which SQL clause is used for filtering?",
            "options": ["WHERE", "GROUP BY", "HAVING"],
            "answer": "WHERE",
        },
        {
            "question": "Which database model uses tables?",
            "options": ["Relational", "Hierarchical", "Graph"],
            "answer": "Relational",
        },
        {
            "question": "What is a foreign key?",
            "options": ["Reference key", "Primary key", "Unique key"],
            "answer": "Reference key",
        },
    ],
    "Python": [
        {
            "question": "What is the output of '3 * 'abc'?",
            "options": ["'abcabcabc'", "'abc*3'", "Error"],
            "answer": "'abcabcabc'",
        },
        {
            "question": "Which of these is a mutable type?",
            "options": ["Tuple", "List", "String"],
            "answer": "List",
        },
        {
            "question": "Which is used to convert a string to lowercase?",
            "options": ["lower()", "downcase()", "toLower()"],
            "answer": "lower()",
        },
        {
            "question": "Which of these is a loop structure?",
            "options": ["if", "for", "print"],
            "answer": "for",
        },
        {
            "question": "Which method is used to add an element to a list?",
            "options": ["add()", "append()", "insert()"],
            "answer": "append()",
        },
        {
            "question": "What is a lambda function?",
            "options": ["Anonymous function", "Recursive function", "Static function"],
            "answer": "Anonymous function",
        },
        {
            "question": "What is the keyword for defining a function?",
            "options": ["function", "def", "lambda"],
            "answer": "def",
        },
        {
            "question": "Which module is used for JSON in Python?",
            "options": ["json", "os", "sys"],
            "answer": "json",
        },
        {
            "question": "How do you declare a dictionary?",
            "options": ["{}", "[]", "set()"],
            "answer": "{}",
        },
        {
            "question": "Which statement is used to handle exceptions?",
            "options": ["try-except", "try-finally", "except-finally"],
            "answer": "try-except",
        },
    ],
}

# User registration
def register():
    print("Enter your details to register:")
    name = input("Full Name: ")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")

    query = (
        "INSERT INTO users (name, username, password, email) VALUES (%s, %s, %s, %s)"
    )
    cursor.execute(query, (name, username, password, email))
    db.commit()
    print("Registration successful!")


# User login
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    if user:
        print("Login successful!")
        return username
    else:
        print("Login failed. Please check your username and password.")
        return None


# Quiz attempt
def attempt_quiz():
    username = login()
    if not username:
        return
    subject = input("Choose a subject: DSA, DBMS, Python: ").strip()
    if subject not in quizzes:
        print("Invalid subject choice.")
        return
    score = 0
    selected_questions = random.sample(quizzes[subject], 5)  # Select 5 random questions
    for q in selected_questions:
        print("\n" + q["question"])
        for i, option in enumerate(q["options"], start=1):
            print(f"{i}. {option}")
        answer = input("Enter the option number of your answer: ").strip()
        if q["options"][int(answer) - 1] == q["answer"]:
            score += 1
    print(f"\nYou scored {score} out of {len(selected_questions)}.")

    query = "INSERT INTO results (username, subject, score) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, subject, f"{score}/{len(selected_questions)}"))
    db.commit()
    print("Your result has been saved.")


# Show all results
def show_results():
    print("\n--- Results ---")
    query = "SELECT * FROM results"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"Name: {row[1]}, Subject: {row[2]}, Score: {row[3]}")


# Main function to display options
def main():
    while True:
        op = input(
            """\nChoose an option: 
        1. Register
        2. Login
        3. Attempt Quiz
        4. Show Results
        5. Exit
        Enter your choice: """
        )
        if op == "1":
            register()
        elif op == "2":
            login()
        elif op == "3":
            attempt_quiz()
        elif op == "4":
            show_results()
        elif op == "5":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")


main()
