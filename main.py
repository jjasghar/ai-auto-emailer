#!/usr/bin/env python
import csv
from ollama import chat
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import markdown

port = 465
password = input("SMTP password: ")
sender_email = "postmaster@asgharlabs.io"

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("email.html.j2")

with open("names.csv") as data_file:
    data = csv.DictReader(data_file)
    data_list = []
    for row in data:
        data_list.append(row)

template_email = """
DevOpsDays Austin is in its thirteenth year, and we are one of the oldest DevOpsDays in the United States and the world. We consistently are near or at capacity on tickets sold (~320-400, depending on our venue) and have 90% or greater of attendees check in. Attendees skew toward more experienced and range from senior engineer to director to CEO, and they represent companies from stealth startups to large enterprises with sectors like finance, healthcare, and as-a-service platforms.

In our survey of attendees last year, one piece of feedback we received was literally "Would have liked more vendors to interact with," and that was for a sold-out sponsorship area. Our community appreciates our sponsors and wants to interact with you. We would love to have you.
"""

prospectus = "https://assets.devopsdays.org/events/2025/austin/devopsdays-austin-2025-sponsor-prospectus.pdf"

date_of_event = "May 1st, and 2nd, 2025"

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.mailgun.org", port, context=context) as server:
    server.login("postmaster@asgharlabs.io", password)

    for i in data_list:

        receiver_email = i['email']

        response = chat(model='granite3.2', messages= [
        {
            'role': 'user',
            'content': f"You are a professional cold caller for events. You write friendly engaging emails to help drive people to want to sponser your events. You use the following information and template email to help write out unique and engaging conversational emails: {template_email}. The date for the event is: {date_of_event}, and if you want to link to the prospectus it is located here: {prospectus}. Write an email that convinces me to want to sponsor this event. The recipients name is {i['name']}. The from is my name as JJ Asghar, and my email address and jjasghar@gmail.com, my phone number is 512-619-0722. Please do not put the Subject at the top of the email.",
        },]
    )

        message = MIMEMultipart("alternative")
        message["Subject"] = "Exclusive Sponsorship Opportunity at DevOpsDays Austin 2025"
        message["From"] = sender_email
        message["To"] = receiver_email

        raw_response =  response['message']['content']
        text_email = raw_response

        markdown_email = markdown.markdown(raw_response)
        html_email = template.render(content=markdown_email)
        part1 = MIMEText(text_email, "plain")
        part2 = MIMEText(html_email, "html")

        message.attach(part1)
        message.attach(part2)

        #print(response['message']['content'])
        server.sendmail(sender_email, receiver_email, message.as_string())
        print(f">>>> email sent to {i['email']} <<<<<")

