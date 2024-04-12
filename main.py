import streamlit as st
import pandas as pd

def main():

    st.set_page_config(
       page_title="PDEU Project Portal",
       page_icon="https://media.licdn.com/dms/image/C4E0BAQHHjaeKYhCfPw/company-logo_200_200/0/1630627281515/pdeuofficial_logo?e=1721260800&v=beta&t=MpEH9bd2lJk_tV8uXa54eA81Ef30h6Qy6z7JsRFIh78",
       layout="wide",
       initial_sidebar_state="expanded",
    )
    st.title("Project Portal")


    st.markdown("""
    Welcome to the Project Portal! This portal allows students & faculties to post their project requirements
    and view projects posted by others. Whether you're looking for collaborators or showcasing
    your projects, this platform is designed to facilitate connections and foster collaboration.
    """)

    # Sidebar with action selection
    action = st.sidebar.selectbox("Select an action", ["Post a Project", "View Projects"])

    if action == "Post a Project":
        post_project()

    elif action == "View Projects":
        view_projects()

def post_project():
    st.header("Post a Project")
    role_required = st.text_input("Role Required (optional)[e.g., UI/UX Designer, Backend Developer, etc]", "")
    project_description = st.text_area("Project Description*", "")
    name = st.text_input("Name*")
    email_id = st.text_input("Email ID*", "")
    mobile = st.text_input("Mobile No (Optional)")

    if st.button("Post"):
        # Validate compulsory fields
        if not (project_description and name and email_id):
            st.warning("Please fill in all compulsory fields.")
        # Validate email format
        elif "@" not in email_id:
            st.warning("Enter a valid email.")
        else:
            # Store project details
            save_project(role_required, project_description, name, email_id, mobile)
            st.success("Project Posted Successfully!")

def view_projects():
    st.header("View Projects")
    projects = load_projects()
    if not projects.empty:
        projects.index = range(1, len(projects) + 1)  # Start index from 1
        # Replace empty role required values with "Not Mentioned"
        projects["Role Required"] = projects["Role Required"].fillna("Not Mentioned")
        # Replace empty mobile numbers with "Not Disclosed"
        projects["Mobile No"] = projects["Mobile No"].fillna("Not Disclosed")
        st.table(projects)
    else:
        st.warning("No projects posted yet.")

def save_project(role_required, project_description, name, email_id, mobile):
    # Create or load existing projects dataframe
    try:
        projects = pd.read_csv("projects.csv")
    except FileNotFoundError:
        projects = pd.DataFrame(columns=["Role Required", "Project Description", "Name", "Email ID", "Mobile No"])

    # Add new project if compulsory fields are filled
    if project_description and name and email_id:
        new_project = pd.DataFrame({"Role Required": [role_required],
                                     "Project Description": [project_description],
                                     "Name": [name],
                                     "Email ID": [email_id],
                                     "Mobile No": [mobile]})
        projects = pd.concat([projects, new_project], ignore_index=True)

        # Save projects dataframe
        projects.to_csv("projects.csv", index=False)
    else:
        st.warning("Cannot save project. Please fill in all compulsory fields.")

def load_projects():
    try:
        projects = pd.read_csv("projects.csv")
        return projects
    except FileNotFoundError:
        return pd.DataFrame()

if __name__ == "__main__":
    main()
