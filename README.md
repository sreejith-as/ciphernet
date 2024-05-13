# Ciphernet


<p align="center"> <img src="https://github.com/stanboii/ciphernet/assets/108393479/cfa58799-1f1a-41e3-953b-4c3ff60dcb38" height=100 /> </p>
<br>






<p align="center">
<a href="https://www.python.org/"><img src="https://forthebadge.com/images/badges/made-with-python.svg" border="0" title="Made with Python" />
</p>

<p align="center">
<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." /></a>
</p>


### Modules
- User
- Admin

### Pages
- Login Page
- Signup Page
- Create Profile Page
- Edit Profile Page
- Create Post Page
- Post Details Page
- Delete Post Page
- Update post page
- Password Reset Page
- Username Reset Page
- Feed/Home page
- User Profile Page
- Search Results Page
- Post Comment Page
- Saved Post page
- Report Post page
- Chat Page
- Admin Login Page
- Admin Home Page
- Admin Usersinfo Page
- Admin Reports Page

### Features

- Follow/Unfollow Users
- Like/Unlike the Posts
- Delete/Update the Posts
- Download the post images
- Comment on user posts
- Save Posts
- User suggestion section
- Search users/tags through the search bar
- Report Posts/Users
- Chat with other users
- Change username/password
- Email authentication
- Password reset through email

### Tools and Techs

Backend Framework: `Django`
<br/><br/>
Front-end : `Bootstrap, SCSS, HTML,CSS, Javascript`
<br/><br/>
Database: `Sqlite3`
<br/><br/>

### Installation

1. - Fork the [repo](https://github.com/stanboii/ciphernet)
   - Clone the repo to your local system
   ```git
   git clone https://github.com/stanboii/ciphernet.git
   ```
   Make sure you have python installed on your system.
2. Create a Virtual Environment for the Project

   If u don't have a virtualenv installed

   ```bash
   pip install virtualenv
   ```
   **For Windows Users**
   ```bash
   virtualenv env
   env/Scripts/activate
   ```


   **For Linux Users**
   ```bash
   virtualenv env
   source env/Scripts/activate
   ```

   If you are giving a different name than `env`, mention it in `.gitignore` first

3. Install all the requirements

   ```bash
   pip install -r requirements.txt
   ```

4. Make migrations/ Create db.sqlite3

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a super user.
   This is to access Admin panel and admin specific pages.

   ```djangotemplate
   python manage.py createsuperuser
   ```
   

   Enter your username, email and password.

6. Run server
   ```bash
   python manage.py runserver
   
