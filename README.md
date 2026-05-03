# Vrat Quest (Fasting Simulator) 🍎🧘‍♂️

Vrat Quest is a high-paced, arcade-style web game where the objective is to maintain your fast by catching permitted "Sattvic" foods while dodging prohibited items!

Built entirely with HTML5 Canvas, Vanilla JavaScript, and CSS, the game requires no installation or build steps and can be played directly in your browser.

## 🎮 How to Play

Items will fall from the sky. You control the basket/character at the bottom of the screen.

**Controls:**
- **Desktop**: Use the **Left** and **Right Arrow Keys** to move. You can also click and drag your mouse.
- **Mobile/Tablet**: Touch and drag anywhere on the game screen to move your character.

### Item Classifications

| Category | Items | Effect |
| :--- | :--- | :--- |
| **Sattvic (Permitted)** | 🍎 Apple | **+10 Score** and fills the Vrat Meter. Catch these to maintain your fast! |
| **Junk (Prohibited)** | 🍔 Burger | **-1 Life**. Instantly breaks your fast. If you lose all 3 lives, it's Game Over! |
| **Non-Vrat (Grains)** | 🌾 Wheat Bowl | **-5 Score Penalty**. Avoid these distractions! |

## 🚀 How to Run Locally

Since this is a static web application, running it is incredibly simple:

1. Clone or download this repository.
2. Open the directory in your terminal.
3. Start a local web server. For example, using Python or npx:
   ```bash
   # Using npx (Node.js)
   npx http-server -p 8080

   # Or using Python 3
   python3 -m http.server 8080
   ```
4. Open your browser and navigate to `http://localhost:8080`.

## 🌐 Deploying to GitHub Pages

This game is perfectly structured to be hosted for free on GitHub Pages:

1. Push this entire project to a new public repository on GitHub.
2. Go to the repository's **Settings** tab.
3. Click on **Pages** in the left sidebar.
4. Under "Build and deployment", set the **Source** to "Deploy from a branch".
5. Select your `main` or `master` branch and click **Save**.
6. Within a few minutes, your game will be live at `https://<your-username>.github.io/<repository-name>/`!

## 🛠 Technology Stack

- **Core Mechanics**: Vanilla JavaScript with `requestAnimationFrame` for a smooth game loop.
- **Rendering**: HTML5 `<canvas>` API.
- **Styling**: Modern CSS3 with Flexbox and Glassmorphism overlays (`backdrop-filter`).
- **Assets**: AI-generated 2D game sprites designed with vibrant traditional and arcade motifs.
