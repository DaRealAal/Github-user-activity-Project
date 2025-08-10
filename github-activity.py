from sys import argv
from requests import get

# Github: @DaRealAal
# Project: GitHub User Activity

# Makes text red and rsets the color at the end of the line
red_text_color = '\033[31m'
reset_color = '\033[0m'

#Defines a get user data
def get_user_data(username):
    # creating a url for endpoint to fetch the user’s activity
    fetch_user_activity = f"https://api.github.com/users/{username}/events"
    # Stores the activitys in a list so that I can later print it
    list_activity = []

    try:
        # Begin requesting to the server
        request_user_activity = get(fetch_user_activity)

        if check_connection_url(request_user_activity):

            """
            json data that the request_user_activity we requested will show a json data,
            so I had to store it into a json file and I treat it as a dictionary.
            """

            json_data: dict = request_user_activity.json()

            # Looping through every each activity and adds that to the list_activity
            for data in json_data:
                if data["type"] == "IssuesEvent":
                    list_activity.append(
                        "Opened a new issue in {} | {}".format(data["repo"]["name"], data['payload']['issue']['created_at'])
                    )
                elif data["type"] == "PushEvent":
                    list_activity.append(
                        "Pushed a new repository to {} | {}".format(data["repo"]["name"], data['created_at'])
                    )
                elif data["type"] == "PullRequestEvent":
                    list_activity.append(
                        "Pushed {} commits to {} | {}".format(
                            data["payload"]["pull_request"]["commits"],
                            data["repo"]["name"],
                            data['payload']['pull_request']['created_at']
                        )
                    )
                elif data["type"] == "WatchEvent":
                    list_activity.append("Starred {} | {}".format(data['repo']['name'], data['created_at']))
                elif data["type"] == "ReleaseEvent":
                    list_activity.append("Released a new build on {} | {}".format(data['repo']['name'], data['payload']['issue']['created_at']))
                elif data["type"] == "ForkEvent":
                    list_activity.append("forked {} | {}".format(data['repo']['name'], data['payload']['issue']['created_at']))

        else:
            # Prints only if the username is not a valid
            print(red_text_color + "Username doesnt exist.. Please try another one" + red_text_color)
    
    # Exception that causes issue with network
    except Exception as e:
        print("%s An error as occurred... %s%s" % (red_text_color, e, reset_color))

    # Finally prints the list actvity
    for data in list_activity:
        print("- " + data)


# Checks the connection to ensure the we are connected otherwise returns false
def check_connection_url(request_url):
    if request_url.status_code == 200:
        return True

    return False


# Weather this is a main window to run or not
if __name__ == '__main__':
    # Grabs the 2nd arguments in the CLI that is username passed in
    username = argv[1]
    # Calls the get user data function to start
    get_user_data(username)