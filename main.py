"""
Synopsis: Creates stable roommate pairings based on
psychological survey results and roommate preferences.
"""

from matching.games import StableRoommates
from functools import cache
import smtplib
import math

"""
Overview: Class of the student object
Arguments: name and suid, both as strings
Returns: When assigned is a student object
"""


class student:
    def __init__(self, name: str, suid: str):
        self.email = suid + "@stanford.edu"
        self.name = name
        self.suid = suid
        self.openess = 0
        self.consci = 0
        self.extra = 0
        self.agree = 0
        self.neuro = 0
        self.clean = 0
        self.noise = 0

    def __eq__(self, other):
        return self.suid == other.suid

    def __hash__(self):
        return hash(self.suid)

    """
    Overview: Gets the similarity between two distinct
    students' OCEAN scores by way of euclidean distance
    Arguments: A student object to be compared to
    Returns: The euclidean distance between students
    """

    #@cache
    def get_similarity(self, other):
        first = [self.openess, self.consci, self.extra, self.agree, self.neuro, self.clean, self.noise]
        second = [other.openess, other.consci, other.extra, -1 * other.agree, other.neuro, other.clean,
                  other.noise]
        return math.sqrt(sum(pow(x - y, 2) for x, y in zip(first, second)))


"""
Overview: Gets all students from survey database
Arguments: None; assumes survey database exists
Returns: List containing all students, classed
"""


def get_students():
    all_students = []
    with open("A - Sheet6.csv", 'r') as file:  # EDIT FILENAME GIVEN FORM
        data = file.readlines()
        for line in data:
            parts = line.split(",")
            new_student = student(parts[1], parts[0])
            student.openess = parts[2]
            student.consci = parts[3]
            student.extra = parts[4]
            student.agree = parts[5]
            student.neuro = parts[6]
            student.clean = parts[7]
            student.noise = parts[8]
            all_students.append(new_student)
    return all_students


"""
Overview: Gets preferences using student OCEAN scores
Arguments: A list containing all student objects
Returns: A dictionary of each student's preferences
"""


def get_preferences(all_students: list):
    preferences = {}
    for student in all_students:
        all_others = [other_student for other_student in all_students if other_student != student]
        all_others.sort(key=student.get_similarity, reverse=True)
        preferences[student] = [other_student.email for other_student in all_others]
    return preferences


"""
Overview: Gets optimal matches for all students
Arguments: A dictionary of student preferences
Returns: A dictionary containing optimal matches
"""


def get_matches(preferences: dict):
    unmatched = StableRoommates.create_from_dictionary(preferences)
    return unmatched.solve()


"""
Overview: Sends matches to participants via email
Arguments: A dictionary of all the valid matches
Returns: Nothing; just sends matches through email
"""


def send_emails(matches: dict):
    sender_email = XXXXXXXXXXXX
    password = XXXXXXXXXXXX
    server = smtplib.SMTP("smtp.gmail.com", 587)
    #server.starttls()
    #server.login(sender_email, password)

    for student in matches:
        receiver_email = f"{student}@stanford.edu"
        message = f"Hi {student}. Your optimal match is {matches[student]}. This matching is not officially affiliated" \
                  f" with Stanford and as such you'll have to reach out to them if you would like to room with them. " \
                  f"Their email is {matches[student]}@stanford.edu"

        #server.sendmail(sender_email, receiver_email, message)

    print("All emails sent")


def send_updated_emails(prefs: dict):
    sender_email = XXXXXXXXXXXX
    password = XXXXXXXXXXXX
    server = smtplib.SMTP("smtp.gmail.com", 587)
    #server.starttls()
    #server.login(sender_email, password)

    for student in prefs:
        receiver_email = f"{student.suid}@stanford.edu"
        message = f"Hi {student.name}. \nSeveral students have asked if they could have access to more matches. We " \
                  f"want you to help you as much as possible, so we have included a list of all students in your " \
                  f"neighborhood looking for a roommate. They are ordered in descending order from most optimal " \
                  f"(left) to least (right). \n\n{prefs[student]} \n\nAs a reminder, this is not officially affiliated" \
                  f" with Stanford, so you'll have to reach out to others that you would like to room with and sign" \
                  f"up using the appropriate measures within the r&de application."
        print(message)
        #server.sendmail(sender_email, receiver_email, message)

    print("All emails sent")


"""
Overview: Executes Stanford Plates
Arguments: No arguments needed
Returns: Runs Stanford Plates
"""


def main():
    # part 1
    #send_emails(get_matches(get_preferences(get_students())))
    #print("Program Completed")

    # second iteration
    student_prefs = get_preferences(get_students())
    print(student_prefs)
    # send_updated_emails(student_prefs)

if __name__ == '__main__':
    XXXXXXXXXXXX = "enter email"
    main()
