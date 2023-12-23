# harvard_final_project_cs50x
A cd online store

<h3>Login page<h3>
<img src="/readme_images/login.jpeg">
<hr>
<h3>Gallery page<h3>
<img src="/readme_images/gallery.jpeg">
<hr>
<h3>Dynamic search page (htmx)<h3>
<img src="/readme_images/dynamic_search.jpeg">
<hr>
<h3>Cart page<h3>
<img src="/readme_images/cart.jpeg">
<hr>
<h3>Profile page (history & password change)<h3>
<img src="/readme_images/profile.jpeg">

This will be an online shop where customers can singn up, log in, browse music cds by artist, album name, see album artwork, order items

<h3>1. I started by donwloading dataset as csv from kaggle, then cleaned it up and saved to sqlite database using script gen_albums.py. Db in use - sqlite. Then I indexed album, artist columns to improve search performance later in app usage</h3>

<h3>2. I started by creating log in system. I wrote login_required decorator, three routes that uses session object to check if user has been logged in. Also session expires in 3600 seconds.</h3>

<h3>3. public and templates foders were created to store media(photos, css, js etc) and template html files</h3>

<h3>4. Added login and register forms. Took free stock image from unsplash, imported tailwind styles, optimized backgorund image size</h3>

<h3>5. Added tables to database to store user login information and orders, also order item</h3>

<h3>6. Added htmx to create dynamic search and some other dynamic content without needing to hard reload the page</h3>

<h3>7. Added Gallery of random chosen albums to be displayed in gallery, added mobile friendly layout, added product cards with javascript auto close functionality<h3>

<h3>8. Added product cart item, cart is being stored in session object, if user orders basket items a new record is written to database.<h3>

<h3>9. Added profile page where user can change his passwod and see order history<h3>

