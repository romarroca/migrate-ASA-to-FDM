import requests

# Suppress insecure requests warning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# FDM API details
FDM_HOST = "https://192.168.8.69"
FDM_USERNAME = "admin"
FDM_PASSWORD = "P@ssw0rd"
AUTH_ENDPOINT = "/api/fdm/v6/fdm/token"
DEPLOY_ENDPOINT = "/api/fdm/v6/operational/deploy"


def get_auth_token():
    """
    Retrieve the authentication token.
    """
    data = {
        "grant_type": "password",
        "username": FDM_USERNAME,
        "password": FDM_PASSWORD
    }
    
    response = requests.post(FDM_HOST + AUTH_ENDPOINT, json=data, verify=False)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        response.raise_for_status()


def deploy_changes(auth_token):
    """
    Deploy changes to the Cisco FDM.
    """
    headers = {
        'Authorization': f"Bearer {auth_token}",
        'Content-Type': 'application/json'
    }
    
    # You might need to adjust the data payload as per your requirements.
    data = {
        "forceRefreshDeploymentData": False,
        "type": "deploymentstatus"
    }

    response = requests.post(FDM_HOST + DEPLOY_ENDPOINT, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        deployment_response = response.json()
        if deployment_response.get('state') == 'QUEUED':
            print("Deployment queued successfully!")
            print(f"Deployment ID: {deployment_response.get('id')}")
        else:
            print(f"Deployment returned with state: {deployment_response.get('state')}")
    else:
        print("Deployment failed!")
        response.raise_for_status()


def main():
    choice = input("Are you sure you want to deploy the pending changes? (yes/no): ").strip().lower()

    if choice == "yes":
        auth_token = get_auth_token()
        deploy_changes(auth_token)
    elif choice == "no":
        print("Deployment aborted!")
    else:
        print("Invalid choice. Please type 'yes' or 'no'.")


if __name__ == "__main__":
    main()
