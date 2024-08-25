Assumed -
I know commiting migration files and env on git is not the correct way but for easiness to setup the project without any issue I have used this Technique   
Attaching the POSTMAN Collection->
    Friend Request Collection - https://lunar-shuttle-800794.postman.co/workspace/Other~0bb5800f-69ac-43d5-baca-57a4cc9dcc88/collection/30994168-e509b640-0d4d-4a6f-86ae-02746cece1a0?action=share&creator=30994168
    User Based Collections- https://lunar-shuttle-800794.postman.co/workspace/Other~0bb5800f-69ac-43d5-baca-57a4cc9dcc88/collection/30994168-5b8ea425-156d-4189-ba9a-3f882eae5878?action=share&creator=30994168
    Friend Request id are used for Friend Request actions 
Follow the Below Steps to setup the application
If you face any issue in setting up the application. Please drop a email to subodhonwork@gmail.com
Please refer the docker file and make sure no other project is running on the same port for Django App, Postgres and Ngnix



Steps to be followed to Setup the Application 
Step 1. Take pull of repository in your local
Step 2. Hit Command -> cd ./user_ticketing
Step 3. Hit command -> docker compose up --build(Make Sure Docker Engine is up and running)
Step 4. Once you are inside the container hit following commands one by one -> python manage.py showmigrations
                                                                            -> ptyhon manage.py makemigrations
                                                                            -> python manage.py migrate
Step 5. Create a super user by using command -> python manage.py createsuperuser
Step 6. Open the Admin Page and see if there is no exception in logs
                                                    


