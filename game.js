const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// UI Elements
const startScreen = document.getElementById('startScreen');
const gameOverScreen = document.getElementById('gameOverScreen');
const startBtn = document.getElementById('startBtn');
const restartBtn = document.getElementById('restartBtn');
const scoreDisplay = document.getElementById('scoreDisplay');
const livesDisplay = document.getElementById('livesDisplay');
const vratFill = document.getElementById('vratFill');
const finalScoreDisplay = document.getElementById('finalScore');

// Assets
const images = {
    bg: document.getElementById('bgImg'),
    player: document.getElementById('playerImg'),
    sattvic: document.getElementById('sattvicImg'),
    junk: document.getElementById('junkImg'),
    nonvrat: document.getElementById('nonvratImg')
};

// Game Constants
const WIDTH = canvas.width;
const HEIGHT = canvas.height;
const PLAYER_SIZE = 70;
const ITEM_SIZE = 50;

// Game State
let gameState = 'MENU'; // MENU, PLAYING, GAME_OVER
let score = 0;
let lives = 3;
let vratMeter = 0;
const MAX_VRAT = 100;

let player = {
    x: WIDTH / 2 - PLAYER_SIZE / 2,
    y: HEIGHT - PLAYER_SIZE - 20,
    width: PLAYER_SIZE,
    height: PLAYER_SIZE,
    speed: 8,
    dx: 0
};

let items = [];
let frames = 0;
let baseSpeed = 4;
let spawnRate = 60; // Spawn an item every X frames
let animationId;

// Input Handling
const keys = {
    ArrowLeft: false,
    ArrowRight: false
};

window.addEventListener('keydown', (e) => {
    if (keys.hasOwnProperty(e.key)) keys[e.key] = true;
});

window.addEventListener('keyup', (e) => {
    if (keys.hasOwnProperty(e.key)) keys[e.key] = false;
});

// Touch/Mouse controls for mobile friendliness
let isDragging = false;
canvas.addEventListener('touchstart', handleTouchStart, {passive: false});
canvas.addEventListener('touchmove', handleTouchMove, {passive: false});
canvas.addEventListener('touchend', () => isDragging = false);

canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    updatePlayerPosFromMouse(e);
});
canvas.addEventListener('mousemove', (e) => {
    if(isDragging) updatePlayerPosFromMouse(e);
});
canvas.addEventListener('mouseup', () => isDragging = false);

function handleTouchStart(e) {
    e.preventDefault();
    isDragging = true;
    updatePlayerPosFromTouch(e);
}
function handleTouchMove(e) {
    e.preventDefault();
    if(isDragging) updatePlayerPosFromTouch(e);
}
function updatePlayerPosFromTouch(e) {
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches[0];
    const x = touch.clientX - rect.left;
    player.x = Math.max(0, Math.min(WIDTH - player.width, x - player.width / 2));
}
function updatePlayerPosFromMouse(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    player.x = Math.max(0, Math.min(WIDTH - player.width, x - player.width / 2));
}

// Button Listeners
startBtn.addEventListener('click', startGame);
restartBtn.addEventListener('click', startGame);

function initGame() {
    score = 0;
    lives = 3;
    vratMeter = 0;
    items = [];
    frames = 0;
    baseSpeed = 4;
    spawnRate = 60;
    player.x = WIDTH / 2 - PLAYER_SIZE / 2;
    updateHUD();
}

function startGame() {
    initGame();
    gameState = 'PLAYING';
    startScreen.classList.remove('active');
    startScreen.classList.add('hidden');
    gameOverScreen.classList.remove('active');
    gameOverScreen.classList.add('hidden');
    
    if (animationId) cancelAnimationFrame(animationId);
    gameLoop();
}

function gameOver() {
    gameState = 'GAME_OVER';
    finalScoreDisplay.innerText = score;
    gameOverScreen.classList.remove('hidden');
    gameOverScreen.classList.add('active');
}

function updateHUD() {
    scoreDisplay.innerText = `Score: ${score}`;
    
    let hearts = '';
    for(let i=0; i<lives; i++) hearts += '❤️';
    livesDisplay.innerText = `Lives: ${hearts}`;

    // Update Vrat Meter
    const percentage = Math.min(100, Math.max(0, (vratMeter / MAX_VRAT) * 100));
    vratFill.style.width = `${percentage}%`;
    
    // Change color based on fullness
    if (percentage >= 100) {
        vratFill.style.background = 'linear-gradient(90deg, #FFD700, #FFF)';
        vratFill.style.boxShadow = '0 0 20px #FFD700';
    } else {
        vratFill.style.background = 'linear-gradient(90deg, #FF9933, #FFD700)';
        vratFill.style.boxShadow = '0 0 10px rgba(255, 153, 51, 0.8)';
    }
}

function spawnItem() {
    const rand = Math.random();
    let type, img;
    
    if (rand < 0.5) {
        type = 'sattvic';
        img = images.sattvic;
    } else if (rand < 0.8) {
        type = 'junk';
        img = images.junk;
    } else {
        type = 'nonvrat';
        img = images.nonvrat;
    }

    items.push({
        x: Math.random() * (WIDTH - ITEM_SIZE),
        y: -ITEM_SIZE,
        width: ITEM_SIZE,
        height: ITEM_SIZE,
        type: type,
        img: img
    });
}

function update() {
    // Player movement
    if (keys.ArrowLeft) player.x -= player.speed;
    if (keys.ArrowRight) player.x += player.speed;

    // Boundaries
    if (player.x < 0) player.x = 0;
    if (player.x + player.width > WIDTH) player.x = WIDTH - player.width;

    // Progressive Difficulty
    frames++;
    if (frames % 600 === 0) { // Every ~10 seconds
        baseSpeed += 0.5;
        spawnRate = Math.max(20, spawnRate - 5);
    }

    if (frames % spawnRate === 0) {
        spawnItem();
    }

    // Update Items
    for (let i = items.length - 1; i >= 0; i--) {
        let item = items[i];
        item.y += baseSpeed;

        // Collision Check (AABB)
        // Adding a slight padding to make it feel fairer
        const padding = 10;
        if (
            player.x < item.x + item.width - padding &&
            player.x + player.width > item.x + padding &&
            player.y < item.y + item.height - padding &&
            player.y + player.height > item.y + padding
        ) {
            // Caught item
            if (item.type === 'sattvic') {
                score += 10;
                vratMeter += 10;
                if (vratMeter > MAX_VRAT) vratMeter = MAX_VRAT;
            } else if (item.type === 'junk') {
                lives--;
                vratMeter = 0; // Reset meter on junk as penalty
                
                // Visual feedback (shake or flash could be added here)
                canvas.style.filter = 'contrast(1.5) sepia(1) hue-rotate(-50deg)';
                setTimeout(() => canvas.style.filter = 'none', 100);

                if (lives <= 0) {
                    gameOver();
                }
            } else if (item.type === 'nonvrat') {
                score = Math.max(0, score - 5);
            }
            
            items.splice(i, 1);
            updateHUD();
            continue;
        }

        // Missed item
        if (item.y > HEIGHT) {
            items.splice(i, 1);
        }
    }
}

function draw() {
    // Clear canvas and draw background
    if (images.bg.complete) {
        ctx.drawImage(images.bg, 0, 0, WIDTH, HEIGHT);
    } else {
        ctx.fillStyle = '#87CEEB';
        ctx.fillRect(0, 0, WIDTH, HEIGHT);
    }

    // Draw Player
    if (images.player.complete) {
        ctx.save();
        // Make the player image circular since it might be a square jpg
        ctx.beginPath();
        ctx.arc(player.x + player.width/2, player.y + player.height/2, player.width/2, 0, Math.PI * 2);
        ctx.closePath();
        ctx.clip();
        ctx.drawImage(images.player, player.x, player.y, player.width, player.height);
        ctx.restore();
    } else {
        ctx.fillStyle = '#0000FF';
        ctx.fillRect(player.x, player.y, player.width, player.height);
    }

    // Draw Items
    items.forEach(item => {
        if (item.img && item.img.complete) {
            // Adding a gentle rotating effect to falling items for polish
            ctx.save();
            ctx.translate(item.x + item.width/2, item.y + item.height/2);
            ctx.rotate((frames % 360) * Math.PI / 180 * (item.type==='sattvic'? 1 : -1) * 0.5);
            ctx.drawImage(item.img, -item.width/2, -item.height/2, item.width, item.height);
            ctx.restore();
        } else {
            ctx.fillStyle = item.type === 'sattvic' ? '#00FF00' : (item.type === 'junk' ? '#FF0000' : '#FFA500');
            ctx.beginPath();
            ctx.arc(item.x + item.width/2, item.y + item.height/2, item.width/2, 0, Math.PI*2);
            ctx.fill();
        }
    });
}

function gameLoop() {
    if (gameState !== 'PLAYING') return;

    update();
    draw();

    animationId = requestAnimationFrame(gameLoop);
}

// Initial draw for background
window.onload = () => {
    draw();
};
