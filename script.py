import json, os
from os import listdir
class Assignment:
    __submitted=[] #Encapsulation

    def submit(self, student, content): #Abstraction
        try:
            with open(f'data/assignments/submission/{self.title}/{student.enrollment_no}.json', 'r+') as f:
                s = json.load(f)     
        except FileNotFoundError:
            s={}
            s['approved'] = False
            s['submission']={"first iteration": content}
            self.__submitted.append(student.enrollment_no)
            self.save()
        s.get('submission')[list(s.get('submission').keys())[-1]]=content
        os.makedirs(f'data/assignments/submission/{self.title}/', exist_ok=True)
        with open(f'data/assignments/submission/{self.title}/{student.enrollment_no}.json', 'w') as f:
            json.dump({
                "submission": s.get('submission'),
                "approved": s.get('approved')
            }, f)
        return f"Assignment {self.title} submitted successfully by {student.name}"

    def save(self):
        with open(f'data/assignments/{self.title}.json', 'w') as f:
            json.dump({
                "reviewer": self.reviewer,
                "title": self.title,
                "content": self.content,
                "submitted": self.__submitted
            }, f)

    def __init__(self, title=None): # Polymorphism
        #to load existing assignment
        if title:
            with open(f'data/assignments/{title}.json', 'r+') as f:
                content = f.read()
                if content:
                    a=json.loads(content)
                else:
                    raise KeyError("assignment's json file empty")
            self.reviewer = a.get('reviewer')
            self.title = a.get('title')
            self.content = a.get('content')
            self.__submitted = a.get('submitted') or []

      
            
    def create_assignment(self, reviewer, title, content):
        #to create new assignment
        self.reviewer=reviewer.enrollment_no
        self.title = title
        self.content = content
        with open(f'data/assignments/{title}.json', 'w') as f:
            json.dump({
                "reviewer": self.reviewer,
                "title": self.title,
                "content": self.content,
                "submitted": self.__submitted
            }, f)
        os.makedirs(f'data/assignments/submission/{title}/', exist_ok=True)


class IMG_Member:
    def __init__(self, name, enrollment_no):
        self.name=name
        self.enrollment_no=enrollment_no

    def get_profile(self):
        return vars(self)

    

class Student(IMG_Member): #Inheritance
    submitted_assignments = []

    def get_profile(self): #Abstraction
        profile = super().get_profile()
        profile['pending assignments'] = self.pending_assignments()

    def submit_assignment(self, assignment_title, content):
        a=Assignment(assignment_title)
        return a.submit(self, content)

    def view_all_submissions(self):
        submissions={}
        for assignment in listdir(f'data/assignments/submission/'):
            try:
                with open(f'data/assignments/submission/{assignment}/{self.enrollment_no}.json', 'r+') as f:
                    submissions[assignment]=json.load(f)
            except FileNotFoundError:
                pass # not submitted this one
        return submissions

    def view_submission(self, assignment_title):
        try:
            with open(f'data/assignments/submission/{assignment_title}/{self.enrollment_no}.json', 'r+') as f:
                return json.load(f)
        except FileNotFoundError:
            print('Assignment not yet submitted')

    def pending_assignments(self):
        pending = []
        for p in listdir(f'data/assignments/submission/'):
            if str(self.enrollment_no)+'.json' not in listdir(f'data/assignments/submission/' + p):
                # print(str(self.enrollment_no)+'.json')
                pending.append(p)
            else:
                with open(f'data/assignments/submission/{p}/{self.enrollment_no}.json') as f:
                    submission = json.load(f)
                    if not submission['approved']:
                        pending.append(p)
        return pending

class Reviewer(IMG_Member):

    def create_assignment(self, title, content):
        na = Assignment()
        na.create_assignment(self, title, content)
        return f"Assignment '{title}' created by {self.name}."

    def view_assignment(self, title):
        with open(f'data/assignments/{title}') as f:
            return json.load(f)

    def approve_submission(self, student_enrollment_no, assignment):
        with open(f'data/assignments/submission/{assignment}/{student_enrollment_no}.json', 'r') as f:
            s=json.load(f)
        s['approved'] = True
        with open(f'data/assignments/submission/{assignment}/{student_enrollment_no}.json', 'w') as f:
            json.dump(s, f)
        return f"Assignment '{assignment}' approved by {self.name}."

    def suggest_iteration(self, student_enrollment, assignment, suggestions):
        with open(f'data/assignments/submission/{assignment}/{student_enrollment}.json', 'r+') as f:
            s=json.load(f)
        s['submission'][suggestions] =None
        s['approved'] = False
        with open(f'data/assignments/submission/{assignment}/{student_enrollment}.json', 'w') as f:
            json.dump(s, f)
        return f"Iteration suggested for Assignment '{assignment}': {suggestions} to {student_enrollment}"

    def view_submissions(self, assignment):
        submissions={}
        for p in listdir(f'data/assignments/submission/{assignment}/'):
            with open(f'data/assignments/submission/{assignment}/'+p, 'r+') as f:
                submissions[p.split('.')[0]]=json.load(f)
        return submissions