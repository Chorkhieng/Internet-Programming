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
### Current Users in Database
You can use any `username` and `password` below to login.
- account_name: `adminUser`
    ```
    username: admin
    password: password
    ```
- account_name: `chorky`
    ```
    username: chorky
    password: chorky@umn
    ```
- account_name: `Sophal Sok`
    ```
    username: SophalPhat
    password: SophalSok@168
    ```
- account_name: `Jing Lee`
    ```
    username: JingLee
    password: JingLee@999
    ```
- account_name: `Savung Neang`
    ```
    username: Savung555
    password: Savung@555
    ```
- account_name: `Hai`
    ```
    username: HaiHai
    password: Hai@1997
    ```
- account_name: `Rithy Suy`
    ```
    username: RithySuy
    password: RithySuy@1995
    ```
In the `login` page, you can also choose `create` option to create a new account. After a new account is created successfully, you can return `login` page and log in through your new `username` and `password`.
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
