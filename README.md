# harvard_final_project_cs50x
This is an online shop where customers can sign up, log in, browse music CDs by artist or album name, view album artwork, and order items.

<h3>Tech stack:</h3>
<p>Flask, Sqlite, Tailwind, Htmx</p>

<h3>Login page<h3>
<p>Uses forms, tailwind, sends request to database and verifies if the requested username and password is correct. If that is true the user is saved in session and redirected to index page</p>
<img src="/readme_images/login.jpeg">
<hr>
<h3>Gallery page<h3>
<p>Fetches random records from database and displays as cards. If user hovers on card it grows. Used tailwind for styling. When user clicks on the item a htmx get request is sent to endpoint to display requested item</p>
<img src="/readme_images/gallery.jpeg">
<hr>
<h3>Dynamic search page (htmx)<h3>
<p>Htmx fetches search results from endpoint on each change in form. If user clicks on form and there is active display card, it deletes the card to make place for search results.</p>
<img src="/readme_images/dynamic_search.jpeg">
<hr>
<h3>Cart page<h3>
<p>Cart items are stored in session object. If user places the order, data is stored in database with customer id, order id, item ids in the order</p>
<img src="/readme_images/cart.jpeg">
<hr>
<h3>Profile page (history & password change)<h3>
<p>User can change the password and view previous orders. Password change is being valdidated and verified. If there is no password / wrong password or new password does not match - error message is being displayed</p>
<img src="/readme_images/profile.jpeg">

<h3>1. I started by downloading a dataset as a CSV from Kaggle, then cleaned it up and saved it to a SQLite database using the script gen_albums.py. The database in use is SQLite. Then I indexed the album and artist columns to improve search performance later in app usage.</h3>

<h3>2. I started by creating a login system. I wrote a login_required decorator, three routes, session object to check if the user has been logged in. Also, the session expires in 3600 seconds.</h3>

<h3>3. Static and templates folders were created to store media (photos, CSS, JS, etc.) and template HTML files.</h3>

<h3>4. Added login and register forms. Took a free stock image from Unsplash, imported Tailwind styles, and optimized the background image size.</h3>

<h3>5. Added tables to the database to store user login information and orders, also order items.</h3>

<h3>6. Added HTMX to create dynamic search and some other dynamic content without needing to hard reload the page.</h3>

<h3>7. Added a gallery of randomly chosen albums to be displayed in the gallery, added a mobile-friendly layout, added product cards with JavaScript auto-close functionality.</h3>

<h3>8. Added product cart item; the cart is being stored in the session object. If the user orders basket items, a new record is written to the database.</h3>

<h3>9. Added a profile page where the user can change his password and see order history.</h3>