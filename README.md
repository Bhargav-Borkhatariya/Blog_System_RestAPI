# Django_Blog_System_RestAPI
Blog System
==================

Authentication App.
Blog App.

1. First User Register your account.
2. Then Active Your Account Using Opt
3. Also Add Forget Password For User
4. Then User Login in System
5. User Add Blog Using Below Fields.

    - author (is ForeignKey Key)
    - title
    - content
    - category
    - imgae
    - status (like 'draft', publish)
    - created_on
    - updated_on

6. api for show all blogs. (only show publish status blog).
7. Update Blog api.
8. soft delete blog api.
9. Implement comments: Allow users to leave comments on blog posts.
10. Send Email to blog owner When visitor add comment on blog.
11. Implement search functionality: Allow users to search for blog posts by title or category.
12. userprofile api (update, soft delete, logout)

# Deploy
For run this we app need to follow steps like.

1. Download zip and extract it.(Also other options, you can find online.)
2. creat virtual enviroment.
``` python -m venv venv ```
* activate enivroment.
MacOS/Linux: ``` source venv/bin/activate```
Windows: ``` lib/bin/activate``` (Not sure.)
3. Install requirements.txt file.
``` pip install -r requirements.txt```
4. Need to change mysql client credintials in setting.py file.
``` username and pass``` 
5. Creat database and tables.
``` python manage.py makemigrations```
``` python manage.py migrate```
6. run development server.
``` python manage.py runserver```

You are good go, open browser and open your localhost url.
Mostly at 127.0.0.0:8000

## Authors

- [@Bhargav](https://github.com/Bhargav-Wappnet)


## 🚀 About Me
I'm a python developer...


# Hi, I'm Bhargav! 👋


## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bhargav-borkhatariya-bb5010195/)


## Support

For support, email bhargav.wappnet@gmail.com or join our Slack channel.
