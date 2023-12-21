# harvard_final_project_cs50x
A cd online store

<img src="/readme_images/login.jpeg">

This will be an online shop where customers can singn up, log in, browse music cds by artist, album name, see album artwork, order items

<h3>1. I started by donwloading dataset as csv from kaggle, then cleaned it up and saved to sqlite database using script gen_albums.py. Then I indexed album, artist columns to improve search performance later in app usage</h3>

<h3>2. I started by creating log in system. I wrote login_required decorator, three routes that uses session object to check if user has been logged in. Also session expires in 3600 seconds.</h3>

<h3>3. public and templates foders were created to store media(photos, css, js etc) and template html files</h3>

<h3>4. Added login and register forms. Took free stock image from unsplash, imported tailwind styles, optimized backgorund image size</h3>

<h3>5. Added tables to database to store user login information and orders, also order item</h3>

<h3>Color Palette:</h3>
<p>
/* CSS HEX */
--ash-gray: #C7D0C4ff;
--gunmetal: #29303Eff;
--cadet-gray: #9AACBAff;
--gray: #6F7A7Dff;
--charcoal: #2D3748ff;
https://coolors.co/c7d0c4-29303e-9aacba-6f7a7d-2d3748
<p>