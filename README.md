<h1>Platformer Game</h1>
<p>Welcome to the Platformer Game repository! This project is a platform game developed in Python using the Pygame library.</p>

<h2>Features</h2>
<ul>
    <li>Graphics and sound with Pygame</li>
    <li>Interactive menu</li>
    <li>Ranking system</li>
    <li>Player movement and animations</li>
    <li>Collision detection</li>
    <li>Item collection</li>
</ul>

<h2>Setup</h2>
<p>To get started, install the necessary dependencies:</p>
<pre><code>pip install pygame</code></pre>

<h2>How to Play</h2>
<p>Run the main script to start the game:</p>
<pre><code>python main.py</code></pre>

<h2>Code Details</h2>
<p>The code is organized into the following sections:</p>
<h3>Imports</h3>
<p>Imports essential libraries like Pygame, sys, random, time, and serial (unused ones have been removed).</p>

<h3>Configuration</h3>
<p>Sets the Pygame window title and gets the screen size.</p>

<h3>Menu Function</h3>
<p>Creates a menu screen with a background image, title, and buttons to play or quit the game. Uses the Button class to handle button interactions.</p>

<h3>Ranking Function</h3>
<p>Displays a ranking screen with player names and times. Opens a text file to read and display existing rankings. Uses the get_font function to create text objects.</p>

<h3>Player Name Input Function</h3>
<p>Prompts the user to enter their name using a text input box. Uses the get_font function to create text objects.</p>

<h3>Update Ranking Function</h3>
<p>Reads existing ranking data from a text file. Updates the ranking with the new player's name and time. Sorts the ranking data based on time.</p>

<h3>Map Loading Function</h3>
<p>Reads a map file and creates a 2D list representing the game map.</p>

<h3>Animation Functions</h3>
<p>Loads animation sprites from a directory. Sets animation frames and durations. Creates a dictionary to store animation data.</p>

<h3>Game Loop</h3>
<p>Initializes the game window and sets up the clock. Loads game assets (images, sounds, fonts). Defines variables for player movement, jumping, and game state. Enters the main game loop:</p>
<ul>
    <li>Processes user input (keyboard) for movement and jumping</li>
    <li>Updates player position based on movement and collisions</li>
    <li>Handles jump logic (gravity and jump height)</li>
    <li>Renders game elements: background image, coins and other collectibles, animated player character, text for score and timer</li>
    <li>Detects collisions with obstacles and collectibles</li>
    <li>Manages level transitions and end game conditions</li>
</ul>

<h2>Contributing</h2>
<p>Contributions are welcome! Feel free to open issues or submit pull requests.</p>

<a href="https://github.com/MateusVega/GameToSenaiExpo" class="button">See the code on GitHub</a>
