<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

</head>
<body>

<h1>MovieHelper: Movie Recommendation System</h1>

<h2>What is a Recommendation System?</h2>
<p>
Recommendation systems are tools that help users discover items of interest by predicting their preferences.
They are widely used in e-commerce, streaming services, social media, and more.
</p>
<p>
There are mainly three types of recommendation systems:
</p>
<ul>
    <li><strong>Content-Based Filtering:</strong> Recommends items similar to those the user liked before, based on item attributes.</li>
    <li><strong>Collaborative Filtering:</strong> Uses preferences from multiple users to find patterns and recommend items.</li>
    <li><strong>Hybrid Systems:</strong> Combine multiple recommendation strategies to improve accuracy.</li>
</ul>

<h2>How MovieHelper Works</h2>
<p>
MovieHelper uses collaborative filtering techniques to recommend movies based on your taste.
By analyzing similarity between movies in terms of user preferences and metadata,
it filters out movies that best match your selection and displays their posters and titles.
</p>

<h2>Run the App</h2>
<pre><code>streamlit run movie.py</code></pre>

<h2>Download Required Files</h2>
<p>
To run the app, download the necessary data files here:<br/>
<a href="https://www.dropbox.com/scl/fo/fl7wn2akx1s2smlcyoljv/AIBBszB_QT47nopLAk6tsa4?rlkey=v5u00j7liptyi2zzwpkayzvqg&st=isyp9622&dl=0" target="_blank" rel="noopener noreferrer">
    Download movie_dict.pkl and similarity.pkl files
</a>
</p>

<div class="center">
    <h2>Demonstration</h2>
    <img class="demo-gif" src="https://media.giphy.com/media/your-demo-gif-url.gif" alt="MovieHelper Demo" />
</div>

</body>
</html>
