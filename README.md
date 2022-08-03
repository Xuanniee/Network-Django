# Network (Django)

## Project Description
Network (Django) is a Twitter-like social network for making posts and following other users.

## Content

### 1. New Post
![Picture of New Post](./media/README/New%20Post.png?raw=true "New Post")
If the User is authenticated, they can make a text-based post by filling in and submitting the form present at the top of the index page as shown in the picture above.

### 2. All Posts
Similarly, on the Index Page, which also serves as the page that shows all the posts available on Network, ordered in reverse chronological order. Each post also includes the Username of the poster, post content, timestamp of the post, and the number of likes the post has.

Clicking on the Username of any user will redirect us to the profile page of the particular user we are looking at.

### 3. Profile Page
![Picture of Profile Page](./media/README/Profile%20Page.png?raw=true "Profile Page")
The Profile Page of any user will display the number of followers, and number of people they are following. It also displays all the posts made by the particular user in reverse chronological order and has a profile picture for the user.

If the User looking at the profile page is authenticated, and the profile does not belong to said user, there will be a "Follow" / "Unfollow" button that allows the user to toggle between following the user, as shown above.

### 4. Following 
![Picture of Following Posts](./media/README/Has%20Following.png?raw=true "Following Posts")
Clicking on the Following link in the Navbar will redirect the User to a page containing posts from all the people that the current user is following, so long as they are authenticated.

![Picture of No Following](./media/README/No%20Following.png?raw=true "No Following")
If the User does not follow anyone, the page will be blank, safe for a notice to inform the User that there are no posts as they are not following anyone.

### 5. Pagination
![Picture of Pagination](./media/README/Pagination.png?raw=true "Pagination")
On any page that lists posts, they are limited to having only 10 posts at any one time. In order to see older posts, user will have to make use of the Pagination Navbar to traverse to the next page of 10 posts.

If the User is on the very first page, the First Button would be disabled as shown in the picture above. The converse is true if the User is on the very last page. Finally, the current page that the User is on is highlighted in blue as a visual indicator.

### 6. Edit Post
![Picture of Edit Post](./media/README/Edit%20Post.png?raw=true "Edit Post")
On any of the posts belonging to the current user, there will be an Edit Button as shown in the picture above. When Edit is clicked, the contents of their post will then be replaced with a textarea that is prepopulated with the original text of the post.

Using Javascript, the User is able to save their edits without requiring a reload of the page. 

Lastly, no user can make use of any other route to edit another user's posts.

### 7. Like & Unlike
![Picture of Likes](./media/README/Liked%20Post.png?raw=true "Liked Post")
There is a "Like" Button attached to every post that allows Users to toggle whether they "like" a particular post. If the post is already liked, the Like Button will become an Unlike Button as shown above.

Using Javascript, we are able to asynchronously update the server about the number of "likes" a post has and reflect the updated number of "likes" without actually refreshing the page.

## Learning Outcomes
* Summarised and Put into practice everything I learnt about the Django Framework.
* Learnt to implement Django and Bootstrap's Pagination so as to create a navigation bar at the bottom to navigate between various pages.
* Practiced using Many to Many Relationships in Django Models so as to implement the Likes and Followers system.
* Learnt how to write my own API Routes.
* Familiarised with how to use Django REST Framework Routers to write my URLs.
* Learnt how to manipulate settings.py so as to initialize the Media Root to allow for Images Use.
* Familiarised with various API Views Django REST Framework had to offer like Viewsets.
* Learnt to make use of Serializers to convert complex data into native Python datatypes like JSON.
* Learnt to make use of Django REST Framework to write my own APIs.

## Video Link
https://youtu.be/a3BG0ykgF4E