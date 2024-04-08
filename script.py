#!/usr/bin/env python3

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
        os.makedirs(f'data/assignments/', exist_ok=True)
        with open(f'data/assignments/{title}.json', 'w') as f:
            json.dump({
                "reviewer": self.reviewer,
                "title": self.title,
                "content": self.content,
                "submitted": self.__submitted
            }, f)
        os.makedirs(f'data/assignments/submission/{title}/', exist_ok=True)


class IMG_Member:
    def __init__(self, enrollment_no, name=None):
        if name:
            self.name=name
            self.enrollment_no=enrollment_no
            os.makedirs(f'data/profile/', exist_ok=True)
            with open(f'data/profile/{enrollment_no}.json', 'w') as f:
                json.dump({
                    'name':self.name,
                    'enrollment_no': self.enrollment_no
                },f)
        else:
            os.makedirs(f'data/profile/', exist_ok=True)
            with open(f'data/profile/{enrollment_no}.json') as f:
                p = json.load(f)
                self.name=p['name']
                self.enrollment_no=p['enrollment_no']
        print(f'logged in as {self.name}')

    def get_profile(self):
        with open(f'data/profile/{self.enrollment_no}.json') as f:
            return json.load(f)

    

class Student(IMG_Member): #Inheritance
    submitted_assignments = []

    def get_profile(self): #Abstraction
        profile = super().get_profile()
        profile['pending'] = self.pending_assignments()
        return profile

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
            return

    def pending_assignments(self):
        pending = []
        os.makedirs(f'data/assignments/submission/', exist_ok=True)
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
        with open(f'data/profile/{self.enrollment_no}.json') as f:
            p=json.load(f)
        with open(f'data/profile/{self.enrollment_no}.json', 'w') as f:
            if p.get('assignments'):
                p['assignments'].append(title)
            else:
                p['assignments']=[title]
            json.dump(p, f)
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

def student_menu(stud):
    while True:
        msg = '\n1) Get profile info\n2) Submit assignment\n3) Show pending assignments\n4) View your all submissions\n5) View specific assignment\'s submission\n'
        inp = input(msg)
        if inp == '1':
            profile = stud.get_profile()
            print(f"Name: {profile['name']}\nEnrollment no: {profile['enrollment_no']}\nPending Assignments: {', '.join(profile['pending'])}")
        elif inp == '2':
            title = input('Title: ')
            print('Work:')
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            content = '\n'.join(lines)
            print(stud.submit_assignment(title, content))
        elif inp == '3':
                print('Pending assignments: ', ', '.join(stud.pending_assignments()) or 'None')
        elif inp == '4':
            subm = stud.view_all_submissions()
            for title, sub in subm.items():
                print(f'{title}:')
                for iteration, work in sub['submission'].items():
                    print(f'\t{iteration}: {work}', end=', ')
                print(f'\n\tapproved: ', sub['approved'])
        elif inp == '5':
            inp = input('Title: ')
            subm = stud.view_submission(inp)
            if subm:
                for iteration, work in subm['submission'].items():
                    print(f'\t{iteration}: {work}', end=', ')
                print(f'\n\tapproved: ', subm['approved'])
            else:
                print('Assignment not yet submitted')

def reviewer_menu(rev):
    while True:
        msg = '\n1) Get profile info\n2) Create new assignment\n3) View all your assignments\n4) View submissions of specific assignment\n'
        inp = input(msg)
        if inp == '1':
            profile = rev.get_profile()
            print(f"Name: {profile['name']}\nEnrollment no: {profile['enrollment_no']}")
        elif inp == '2':
            title = input('Title: ')
            print('Content:')
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            content = '\n'.join(lines)
            print(rev.create_assignment(title, content))
        elif inp == '3':
            a=rev.get_profile()['assignments']
            if a:
                print('Your assignments: ', ', '.join(a))
            else:
                print('No assignments created yet')
        elif inp == '4':
            title = input('Title: ')
            submissions = rev.view_submissions(title)
            if not submissions:
                print(f'No submissions for {title}')
                continue
            for en, subm in submissions.items():
                print(f'Student\'s enrollment no: {en}\nDetails:')
                for iteration, work in subm['submission'].items():
                    print(f'\t{iteration}: {work}', end=', ')
                print(f'\n\tapproved: ', subm['approved'])
            inp = input('\n1) Approve submission\n2) Suggest iteration\nPress enter to go back\n')
            if inp=='1':
                en=input('Enrollment no: ')
                print(rev.approve_submission(en, title))
            if inp=='2':
                en=input('Enrollment no: ')
                print('Suggestion: ')
                lines = []
                while True:
                    line = input()
                    if line:
                        lines.append(line)
                    else:
                        break
                suggestion = '\n'.join(lines)
                rev.suggest_iteration(en, title, suggestion)


if __name__ == '__main__':
    msg = '1) Login as student\n2) Login as reviewer\n3) Create new student\n4) Create new reviewer\n'
    while True:
        inp = input(msg)
        if inp == '1':
            enrollment_no = input('Enrollment no: ')
            try:
                stud = Student(enrollment_no)
            except FileNotFoundError:
                print('No such user exists')
            if (stud):
                student_menu(stud)
        elif inp == '2':
            enrollment_no = input('Enrollment no: ')
            rev = Reviewer(enrollment_no)
            if rev:
                reviewer_menu(rev)
        elif inp == '3':
            enrollment_no = input('Enrollment no: ')
            name = input('Name: ')
            stud = Student(enrollment_no, name)
            student_menu(stud)
        elif inp == '4':
            enrollment_no = input('Enrollment no: ')
            name = input('Name: ')
            rev = Reviewer(enrollment_no, name)
            reviewer_menu(rev)