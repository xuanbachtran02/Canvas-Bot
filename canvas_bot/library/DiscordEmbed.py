import os
import pytz
from canvas_bot.Utils import *
from hikari import Embed, Color
from datetime import datetime

class DiscordEmbed:
    def __init__(self) -> None:
        self.logo = os.environ.get('CANVAS_LOGO_URL')

    @staticmethod
    def create_embed(title, body):
        return Embed(
            title=title,
            description=body,
            color=Color.from_hex_code('#ff3939'),
            timestamp=datetime.now().astimezone()
        )
    
    # course list 
    def courselist_embed(self, course_list: list):
        body = ""
        for course in course_list:
            course_link = f"{os.environ.get('CANVAS_COURSE_BASE_URL')}{course['id']}"
            body += makeBold(f"{course['id']} - {makeLink(course['name'], course_link)}") + '\n'

        return self.create_embed(
            title="Course List",
            body=body,
        ).set_footer(
            text='Canvas',
            icon=self.logo
        )
    
    # due soon
    def duesoon_temp_embed(self):
        return self.create_embed(
            title="Request saved!",
            body="Message is waiting to be updated..."
        ).set_footer(
            text="Sent",
            icon=self.logo
        )

    def duesoon_embed(self, course_title: str, course_id: str, assgn_list: list):
        if assgn_list:
            title = f"Due Within A Day | {len(assgn_list)} assignment(s)"
        else:
            title = "No Assignment Due In A Day"
            
        course_link = f"{os.environ.get('CANVAS_COURSE_BASE_URL')}{course_id}"
        body = makeBold(f'Course: {makeLink(course_title, course_link)}')

        e = self.create_embed(
            title=title,
            body=body,
        ).set_footer(
            text="Last updated",
            icon=self.logo
        )

        for assgn in assgn_list:
            # due time
            tz = pytz.timezone('UTC')
            due_time = datetime.strptime(assgn['due_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=tz)
            due_stamp = int(due_time.timestamp())

            # points
            org_points = assgn['points_possible']
            points = int(org_points) if org_points.is_integer() else org_points 

            # embed body
            body  = f"{makeBold(makeLink(assgn['name'], assgn['html_url']))}\n"
            body += f"{makeBold('Points:')} {points}\n"
            body += f"{makeBold('Due:')} <t:{due_stamp}:f> ({makeBold(f'<t:{due_stamp}:R>')})\n"

            name = makeBold("Quiz" if assgn['is_quiz_assignment'] is True else "Assignment")
            e.add_field(
                name=name,
                value=body
            )
        return e