**Classes**

* **IMG_Member**
    * This is a base class for Student and Reviewer. 
    * It has the following attributes:
        * name (string): Name of the member
        * enrollment_no (string): Enrollment number of the member
    * It has the following method:
        * get_profile(): Returns a dictionary containing the member's name and enrollment number.

* **Student**
    * This class inherits from IMG_Member.
    * It has a class attribute:
        * submitted_assignments (list): A list of assignment titles that the student has submitted.
    * It has the following methods:
        * get_profile (override): Inherits the get_profile method from IMG_Member and adds a new key "pending assignments" which contains a list of pending assignments for the student.
        * submit_assignment(assignment_title, content): Takes the assignment title and content as input and calls the Assignment class's submit method to submit the assignment.
        * view_all_submissions(): Returns a dictionary containing all the assignment submissions for the student.
        * view_submission(assignment_title): Takes the assignment title as input and returns the student's submission for that assignment.
        * pending_assignments(): Returns a list of assignment titles that are pending for the student.

* **Reviewer**
    * This class inherits from IMG_Member.
    * It has the following methods:
        * create_assignment(title, content): Takes the assignment title and content as input and calls the Assignment class's create_assignment method to create a new assignment.
        * view_assignment(title): Takes the assignment title as input and returns the assignment details.
        * approve_submission(student_enrollment_no, assignment): Takes the student's enrollment number and assignment title as input and approves the student's submission for that assignment.
        * suggest_iteration(student_enrollment, assignment, suggestions): Takes the student's enrollment number, assignment title, and suggestion string as input and asks the student to iterate on the assignment based on the suggestions.
        * view_submissions(assignment): Takes the assignment title as input and returns a dictionary containing all the submissions for that assignment.

* **Assignment**
    * This class encapsulates information about an assignment.
    * It has the following attributes:
        * __submitted (list): A private list that stores the enrollment numbers of students who have submitted the assignment (encapsulation).
        * reviewer (string): Enrollment number of the reviewer for the assignment.
        * title (string): Title of the assignment.
        * content (string): Content of the assignment.
    * It has the following methods:
        * submit(student, content): Takes the student object and assignment content as input and submits the assignment for the student.
        * save(): Saves the assignment details to a JSON file.
        * __init__(self, title=None): This constructor is used to load an existing assignment or create a new assignment.

**Functionality**

* The code allows students to submit assignments, view their submitted assignments, and view all assignments.
* It allows reviewers to create assignments, view assignments, approve student submissions, suggest iterations for submissions, and view all submissions for an assignment.
* The code uses JSON files to store assignment details and student submissions.

**PS:**

* The code uses the 4 fundamental Object-Oriented Programming concepts namely inheritance, encapsulation, abstraction, and polymorphism.
* The os library is used for file system operations. 
* The json library is used for working with JSON data.
* Here's a working image of the code

<img class="image-placeholder" src="https://i.imgur.com/XU3kRm4.png" alt="">