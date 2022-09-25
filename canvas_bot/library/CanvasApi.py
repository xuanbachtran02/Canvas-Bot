import os
import requests
from datetime import datetime, timedelta

class CanvasApi:
    def __init__(self):
        self.TOKEN = os.environ.get('CANVAS_TOKEN')
        self.BASEURL = 'https://deanza.instructure.com'
        self.HEADERS = {"Authorization": f"Bearer {self.TOKEN}"}
        self._all_course_id = self._get_all_course_id()

    # TODO: cover excpetions
    def _get_all_courses_raw(self, body):
        res = requests.get(
            f'{self.BASEURL}/api/v1/users/self/courses', 
            headers=self.HEADERS, data=body).json()
        return res

    # TODO: cover excpetions
    def _get_course_assignments(self, course_id, body):
        res = requests.get(
            f'{self.BASEURL}/api/v1/courses/{course_id}/assignments', 
            headers=self.HEADERS, data=body).json()
        return res

    def _get_all_course_id(self) -> set:
        course_id_set = set()
        request_body = {
            'enrollment_type': ['student'],
            'enrollment_state': 'active',
            'per_page': 100  # hard coding: maximum 100 courses (TODO: what if courses >= 100)
        }
        all_courses = self._get_all_courses_raw(request_body)
        for course in all_courses:
            course_id_set.add(str(course['id']))
        return course_id_set
          
    def get_all_active_courses(self, option='list-string'):
        course_list = []
        request_body = {
            'enrollment_type': ['student'],
            'enrollment_state': 'active',
            'per_page': 100  # hard coding: maximum 100 courses (TODO: what if courses >= 100)
        }
        all_courses = self._get_all_courses_raw(request_body)
        for course in all_courses:
            if option == 'list-dict':
                course_list.append({'id': str(course['id']), 'name': course['name']})
            elif option == 'list-string':
                course_list.append(f"{course['id']} - {course['name']}")
        return course_list

    # TODO: maybe add optional param for number of days before due
    def get_due_within_day(self, course_id):
        assgn_due_within_day = []
        now = datetime.utcnow()
        request_body = {"order_by": "due_at", "bucket": "upcoming"}

        # exception
        if course_id not in self._all_course_id:
            raise Exception("You don't have access to course with given ID")

        all_assgn = self._get_course_assignments(course_id, request_body)
        for assgn in all_assgn:
            due = datetime.strptime(assgn['due_at'], '%Y-%m-%dT%H:%M:%SZ') 
            if due - now <= timedelta(days=1):
                assgn_due_within_day.append(assgn)
            else:
                break
        return assgn_due_within_day