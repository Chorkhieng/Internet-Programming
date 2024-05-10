# Final-Project
This is a simple social media platform
## Some functionalities for this website
### Login feature
When the users try to access this website, there will be a login page that has two options (login with username and password, or create a new account). Notice that there is no email or personal information required here, and users can just create their own username and password to have access to the site. 

### User interaction
Users can post and edit, comment on post(s), and like posted content(s). However, post editing or deleting is associated only with specific user, which mean users can only edit and delete their post(s).
- Users can comment and like any post, but they are not allowed to edit or delete other users' posts.
- Users can edit or delete their post(s) if they are the author of that post.
- Users can create a new post as desired.
- Users can also sort posts by `newest posts` or by `like count`.
- Current user will be able to see their profile page.
- Current logged-in user will have a `log out` option when they want to sign out of the website.

### Back-end 
This site uses `mysql` for managing database and back-end of the server.

#### Data Storage
- Users Information: For this project users' data contains `user id`, `username`, and `password`.
- Posts: Each post has `post date-time`, `post content`, `post id`, `author's id`, and `like count` associated with it.
- Comments: Each comment is associated with `post id` and `author id` along with `commenter id`.

## How to run this program
### Requirement
Make sure you `expressjs` and `pug` installed other `npm` installation packages
### Get it to work
This instruction requires you to run the program through `ssh-tunnel`
- Go to project folder
- Open a terminal in the project folder and run the following command: 
    ```
    node tunnel.js
    ```
    This will allow you run the program and use my `UMN` databse.
- Open another terminal in the same folder and run the following command:
    ```
    node server.js
    ```
    This will run the `server` for the website
- On your browser, go to the following site:
    ```
    localhost:4131
    ```
    Now you see the login page that allows your to login or create a new account.
