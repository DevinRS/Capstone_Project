# Capstone_Project_TEAM_14
EECS581 Capstone Project

Group Members: Devin, Hubert, Nick, Cody, Tristan
# Sprint 4 Deliverables 

For this sprint, the codebase is available in /backend_app directories.
The full website can be accessed [here](https://mlsandbox.streamlit.app/)

To run the code locally, you need to install uvicorn (pip install uvicorn).

Run the following: uvicorn backend_app.main:app --reload

Test on: .../docs


<h3>Database Implementation</h3>
These methods were implemented using FastAPI, PyDantic, and SQLAlchemy. FastAPI serves our API endpoints, SQLAlchemy performs our database queries, and PyDantic enforces our JSON types.

![image](https://github.com/DevinRS/Capstone_Project/assets/103350414/3567deb9-92f1-479a-afa8-c09580ab6a26)

Here is the our Database Schema. We created 4 tables, 3 of which are connected to the "users" table. The relationship between users and the other tables are one-to-many. 

![image](https://github.com/DevinRS/Capstone_Project/assets/103350414/f10b4022-e8cb-4ede-80a3-d1965d1fc97b)

# Requirement Stack - Sprint 4 

![image](https://github.com/DevinRS/Capstone_Project/assets/103350414/067a62a3-582e-448d-976f-c0b554d067eb)




