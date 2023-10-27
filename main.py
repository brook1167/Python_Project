
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def job_search(userInput):
    url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={userInput}&txtLocation='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    job_details = []
    for job in jobs:
        job_title = job.find('a').text.strip()
        job_company_name = job.find('h3', class_="joblist-comp-name").text.strip()
        job_location = job.find('span').text.strip()
        job_skills = job.find('span', class_="srp-skills").text.replace(' ', '')
        job_more_detail = job.find('a')['href']

        job_details.append({
            'job_title': job_title,
            'job_company_name': job_company_name,
            'job_location': job_location,
            'job_skills':job_skills,
            'job_link':job_more_detail


        })

    return job_details


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        job_details = job_search(name)
        return render_template('form.html', job_details=job_details)
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True,port=5000)
