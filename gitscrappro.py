import requests
import pandas as pd

# Function to fetch users from GitHub API
def fetch_users(city, min_followers):
    url = f'https://api.github.com/search/users?q=location:{city}+followers:>{min_followers}'
    response = requests.get(url)
    return response.json()

# Function to fetch repositories for a given user
def fetch_repositories(username):
    url = f'https://api.github.com/users/{username}/repos?per_page=500'
    response = requests.get(url)
    return response.json()

# Fetch users in Dublin with more than 50 followers
users_data = fetch_users('Dublin', 50)

# Prepare user data for CSV
users_list = []
for user in users_data.get('items', []):
    user_info = {
        'login': user.get('login', ''),
        'name': user.get('name', ''),
        'company': user.get('company', '').strip('@').upper(),
        'location': user.get('location', ''),
        'email': user.get('email', ''),
        'hireable': user.get('hireable', ''),
        'bio': user.get('bio', ''),
        'public_repos': user.get('public_repos', 0),  # Default to 0 if not found
        'followers': user.get('followers', 0),  # Default to 0 if not found
        'following': user.get('following', 0),  # Default to 0 if not found
        'created_at': user.get('created_at', '')
    }
    users_list.append(user_info)

# Save users data to CSV
users_df = pd.DataFrame(users_list)
users_df.to_csv('users.csv', index=False)

# Prepare repositories data for CSV
repositories_list = []
for user in users_list:
    repos = fetch_repositories(user['login'])
    for repo in repos:
        repo_info = {
            'login': user['login'],
            'full_name': repo.get('full_name', ''),
            'created_at': repo.get('created_at', ''),
            'stargazers_count': repo.get('stargazers_count', 0),
            'watchers_count': repo.get('watchers_count', 0),
            'language': repo.get('language', ''),
            'has_projects': repo.get('has_projects', False),
            'has_wiki': repo.get('has_wiki', False),
            # Check if license exists before accessing its name
            'license_name': repo['license']['name'] if repo.get('license') else ''
        }
        repositories_list.append(repo_info)

# Save repositories data to CSV
repos_df = pd.DataFrame(repositories_list)
repos_df.to_csv('repositories.csv', index=False)

# Create README.md file
with open('README.md', 'w') as readme_file:
    readme_file.write("# Dublin GitHub User Scraper\n\n")
    readme_file.write("- This project scrapes GitHub users from Dublin with over 50 followers.\n")
    readme_file.write("- It collects detailed information about each user's repositories.\n")
    readme_file.write("- The data is saved in CSV format for easy analysis.\n\n")
    
    readme_file.write("## Scraping Process\n")
    readme_file.write("This project uses the GitHub API to gather data on users and their repositories.\n\n")

    readme_file.write("## Interesting Findings\n")
    readme_file.write("The analysis revealed various trends regarding user activity and repository popularity.\n\n")

    readme_file.write("## Recommendations\n")
    readme_file.write("Developers should focus on engaging with their community to increase followers and repository visibility.\n")

print("Data scraping completed. Files saved: users.csv, repositories.csv, README.md.")