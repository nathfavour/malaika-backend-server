import requests

BASE_URL = "http://localhost:5000"  # Update with your API base URL

def main():
    while True:
        print("Choose an action:")
        print("1. Create or Get Project")
        print("2. Contribute")
        print("3. Get All Projects")
        print("4. Filter Contributions by Project Title")
        print("5. Get Contributed Project Addresses")
        print("6. Get Contributed Projects")
        print("7. Filter Projects by Address")
        print("8. Filter Projects by Title")
        print("9. Delete Project")
        print("10. Update Project")
        print("11. Transfer Ownership")
        print("0. Exit")
        
        choice = input("Enter the action number: ")
        
        if choice == "0":
            print("Exiting...")
            break
        
        elif choice == "1":
            create_or_get_project()
        
        elif choice == "2":
            contribute()
        
        elif choice == "3":
            get_all_projects()
        
        elif choice == "4":
            filter_contributions_by_project_title()
        
        # Add other choices here
        
        else:
            print("Invalid choice. Please choose a valid action.")

def create_or_get_project():
    project_data = {
    "project_title": input("Enter project title: "),
    "nickname": input("Enter nickname: "),
    "project_description": input("Enter project description: "),
    "project_category": input("Enter project category: "),
    "project_target": float(input("Enter project target: ")),
    "minimum_buy_in": float(input("Enter minimum buy-in: ")),
    "roi": float(input("Enter ROI: ")),
    "stake_amount": float(input("Enter stake amount: ")),
    "photo": input("Enter photo URL: "),
}

    response = requests.post(f"{BASE_URL}/create_or_get_project", json=project_data)
    print(response.json())

def contribute():
    contribution_data = {
        "contributor_address": input("Enter contributor address: "),
        "project_title": input("Enter project title: "),
        "contribution_amount": float(input("Enter contribution amount: ")),
    }
    response = requests.post(f"{BASE_URL}/contribute", json=contribution_data)
    print(response.json())

def get_all_projects():
    response = requests.get(f"{BASE_URL}/get_all_projects")
    print(response.json())

def filter_contributions_by_project_title():
    project_title = input("Enter the project title: ")
    response = requests.get(f"{BASE_URL}/filter_contributions_by_project_title?project_title={project_title}")
    print(response.json())

def get_contributed_project_addresses():
    contributor_address = input("Enter contributor address: ")
    response = requests.get(f"{BASE_URL}/get_contributed_project_addresses?contributor_address={contributor_address}")
    print(response.json())

def get_contributed_projects():
    contributor_address = input("Enter contributor address: ")
    response = requests.get(f"{BASE_URL}/get_contributed_projects?contributor_address={contributor_address}")
    print(response.json())

def filter_projects_by_address():
    address = input("Enter address: ")
    response = requests.get(f"{BASE_URL}/filter_projects_by_address?address={address}")
    print(response.json())

def filter_projects_by_title():
    project_title = input("Enter project title: ")
    response = requests.get(f"{BASE_URL}/filter_projects_by_title?project_title={project_title}")
    print(response.json())

def delete_project():
    project_title = input("Enter project title: ")
    response = requests.delete(f"{BASE_URL}/delete_project", json={"project_title": project_title})
    print(response.json())

def update_project():
    project_data = {
        "project_title": input("Enter project title: "),
        # Provide fields to update
    }
    response = requests.put(f"{BASE_URL}/update_project", json=project_data)
    print(response.json())

def transfer_ownership():
    transfer_data = {
        "project_title": input("Enter project title: "),
        "new_address": input("Enter new address: ")
    }
    response = requests.put(f"{BASE_URL}/transfer_ownership", json=transfer_data)
    print(response.json())
# Add other functions for other actions here

if __name__ == "__main__":
    main()
