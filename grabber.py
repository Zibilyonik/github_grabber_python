# Python3
'''
    this is a webscraper that will grab projects from given user's Github page
    and will create a file with the project name and the link to the project
    
    functions:
        load_user() - asks for user input and returns the user's github name
        load_url(user) - returns the provided user's repos as json
        create_file(data) - creates a file with the project name and the link to the project
        main() - main function
'''
import requests
import bs4


def load_user():
    '''asks for user input and returns the user's github name'''
    user = input("Enter the user's Github name: ")
    return user


def load_url(user):
    '''returns the provided user's repos as json'''
    url = f'https://api.github.com/users/{user}/repos'
    response = requests.get(url, timeout=5)
    data = response.json()
    return data


def create_file(data):
    '''creates a file with the project name and the link to the project'''
    with open('projects.txt', 'w', encoding='utf-8') as file:
        for project in data:
            file.write(f'{project["name"]} - {project["html_url"]}\n')
            file.write(f'{project["description"]}\n\n')

def grab_description(url):
    '''grabs the description from the project's page'''
    response = requests.get(url, timeout=5)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    try:
        description = soup.find('p', {'class': 'f4 my-3'}).text
    except:
        description = 'No description provided'
    return description

def main():
    '''main function'''
    user = load_user()
    data = load_url(user)
    for project in data:
        project['description'] = grab_description(project['html_url'])
    create_file(data)


main()
