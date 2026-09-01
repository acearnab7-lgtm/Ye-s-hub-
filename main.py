from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def serve_game():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YE Casino</title>
        <style>
            :root {
                --bg-main: #0f212e;
                --bg-secondary: #1a2c38;
                --bg-card: #2f4553;
                --accent-blue: #1475e1;
                --accent-blue-hover: #4295fa;
                --text-main: #ffffff;
                --text-muted: #b1bad3;
                --red-suit: #ff1f44;
                --black-suit: #0f212e;
            }
            
            body {
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: var(--bg-main);
                color: var(--text-main);
                display: flex;
                flex-direction: column;
                height: 100vh;
                overflow: hidden;
            }

            /* Top Navbar */
            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: var(--bg-secondary);
                padding: 10px 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }
            .logo {
                font-size: 24px;
                font-weight: bold;
                font-style: italic;
            }
            .header-center {
                display: flex;
                align-items: center;
                background: var(--bg-main);
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: 600;
            }
            .header-right {
                display: flex;
                gap: 15px;
                align-items: center;
            }
            .btn-wallet {
                background: var(--accent-blue);
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                cursor: pointer;
            }

            /* Game Area */
            .game-board {
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                position: relative;
                padding: 20px;
            }
            .table-text {
                color: var(--bg-card);
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
                text-align: center;
                margin: 20px 0;
                text-transform: uppercase;
            }
            
            /* Cards & Hands */
            .hand-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
                min-height: 120px;
            }
            .score-bubble {
                background: var(--bg-secondary);
                color: var(--text-main);
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                z-index: 10;
                opacity: 0;
                transition: opacity 0.3s;
            }
            .cards-wrapper {
                display: flex;
                justify-content: center;
            }
            .card {
                width: 70px;
                height: 100px;
                background: white;
                border-radius: 6px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
                box-shadow: -2px 2px 8px rgba(0,0,0,0.4);
                position: relative;
            }
            .card:not(:first-child) {
                margin-left: -35px; /* Overlap effect */
            }
            .card.red { color: var(--red-suit); }
            .card.black { color: var(--black-suit); }
            .card.hidden {
                background: var(--accent-blue);
                color: white;
                border: 2px solid white;
            }

            /* Bottom Controls */
            .controls-section {
                background: var(--bg-secondary);
                padding: 15px;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }
            .bet-btn {
                width: 100%;
                background: var(--accent-blue);
                color: white;
                border: none;
                padding: 15px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 15px;
                cursor: pointer;
            }
            .bet-btn:hover { background: var(--accent-blue-hover); }
            
            .bet-input-row {
                display: flex;
                justify-content: space-between;
                margin-bottom: 15px;
                font-size: 12px;
                color: var(--text-muted);
            }
            .bet-input-box {
                background: var(--bg-main);
                padding: 10px;
                border-radius: 5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }
            
            .action-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            .action-btn {
                background: var(--bg-card);
                color: var(--text-main);
                border: none;
                padding: 12px;
                border-radius: 5px;
                font-weight: bold;
                cursor: pointer;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 5px;
            }
            .action-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }

            /* Bottom Nav Dummy */
            .bottom-nav {
                display: flex;
                justify-content: space-around;
                padding: 15px 0;
                background: var(--bg-main);
                font-size: 10px;
                color: var(--text-muted);
            }
            .nav-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 4px;
            }
        </style>
    </head>
    <body>

        <header>
            <div class="logo">YE</div>
            <div class="header-center">$0.00 🪙</div>
            <div class="header-right">
                <button class="btn-wallet">Wallet</button>
                <span>👤</span>
                <span>🔔</span>
            </div>
        </header>

        <main class="game-board">
            <div class="hand-container">
                <div class="score-bubble" id="dealer-score">0</div>
                <div class="cards-wrapper" id="dealer-cards">
                    </div>
            </div>

            <div class="table-text">
                Blackjack pays 3 to 2<br>
                Insurance pays 2 to 1
            </div>

            <div class="hand-container">
                <div class="score-bubble" id="player-score">0</div>
                <div class="cards-wrapper" id="player-cards">
                    </div>
            </div>
        </main>

        <section class="controls-section">
            <button class="bet-btn" id="btn-bet" onclick="dealGame()">Bet</button>
            
            <div class="bet-input-row">
                <span>Bet Amount</span>
                <span>0.00000000 USDC</span>
            </div>
            <div class="bet-input-box">
                <span>$ 0.00</span>
                <span>🇺🇸 | 1/2 | 2x</span>
            </div>

            <div class="action-grid">
                <button class="action-btn" id="btn-hit" onclick="hit()" disabled>Hit 🗂️</button>
                <button class="action-btn" id="btn-stand" onclick="stand()" disabled>Stand ✋</button>
                <button class="action-btn" disabled>Split 🎴</button>
                <button class="action-btn" disabled>Double x2</button>
            </div>
        </section>

        <nav class="bottom-nav">
            <div class="nav-item"><span>🔍</span> Browse</div>
            <div class="nav-item" style="color: white;"><span>🎰</span> Casino</div>
            <div class="nav-item"><span>⭐</span> For You</div>
            <div class="nav-item"><span>⚽</span> Sports</div>
            <div class="nav-item"><span>💬</span> Chat</div>
        </nav>

        <script>
            let deck = [];
            let playerHand = [];
            let dealerHand = [];
            let gameOver = true;

            const suits = { '♠': 'black', '♥': 'red', '♦': 'red', '♣': 'black' };
            const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];

            function buildDeck() {
                deck = [];
                for (let d = 0; d < 6; d++) {
                    for (let [suit, color] of Object.entries(suits)) {
                        for (let value of values) {
                            deck.push({ value, suit, color });
                        }
                    }
                }
                for (let i = deck.length - 1; i > 0; i--) {
                    let j = Math.floor(Math.random() * i);
                    [deck[i], deck[j]] = [deck[j], deck[i]];
                }
            }

            function getCardValue(card) {
                if (['J', 'Q', 'K'].includes(card.value)) return 10;
                if (card.value === 'A') return 11;
                return parseInt(card.value);
            }

            function calculateScore(hand) {
                let score = 0;
                let aces = 0;
                for (let card of hand) {
                    score += getCardValue(card);
                    if (card.value === 'A') aces += 1;
                }
                while (score > 21 && aces > 0) {
                    score -= 10;
                    aces -= 1;
                }
                return score;
            }

            function renderCard(card, isHidden = false) {
                if (isHidden) {
                    return `<div class="card hidden">YE</div>`;
                }
                return `<div class="card ${card.color}">
                            <div>${card.value}</div>
                            <div>${card.suit}</div>
                        </div>`;
            }

            function updateUI(hideDealerCard = true) {
                // Render Player
                document.getElementById('player-cards').innerHTML = playerHand.map(c => renderCard(c)).join('');
                document.getElementById('player-score').innerText = calculateScore(playerHand);
                document.getElementById('player-score').style.opacity = 1;

                // Render Dealer
                if (hideDealerCard && !gameOver) {
                    document.getElementById('dealer-cards').innerHTML = renderCard(dealerHand[0]) + renderCard(dealerHand[1], true);
                    document.getElementById('dealer-score').innerText = getCardValue(dealerHand[0]);
                } else {
                    document.getElementById('dealer-cards').innerHTML = dealerHand.map(c => renderCard(c)).join('');
                    document.getElementById('dealer-score').innerText = calculateScore(dealerHand);
                }
                document.getElementById('dealer-score').style.opacity = 1;

                // Buttons
                document.getElementById('btn-bet').disabled = !gameOver;
                document.getElementById('btn-bet').innerText = gameOver ? 'Bet' : 'Game in Progress...';
                document.getElementById('btn-hit').disabled = gameOver;
                document.getElementById('btn-stand').disabled = gameOver;
            }

            function dealGame() {
                buildDeck();
                playerHand = [deck.pop(), deck.pop()];
                dealerHand = [deck.pop(), deck.pop()];
                gameOver = false;
                
                if (calculateScore(playerHand) === 21) {
                    gameOver = true;
                    setTimeout(() => alert("BLACKJACK!"), 500);
                    updateUI(false);
                } else {
                    updateUI(true);
                }
            }

            function hit() {
                playerHand.push(deck.pop());
                if (calculateScore(playerHand) > 21) {
                    gameOver = true;
                    setTimeout(() => alert("Bust! Dealer Wins."), 500);
                    updateUI(false);
                } else {
                    updateUI(true);
                }
            }

            function stand() {
                while (calculateScore(dealerHand) < 17) {
                    dealerHand.push(deck.pop());
                }
                
                let pScore = calculateScore(playerHand);
                let dScore = calculateScore(dealerHand);

                gameOver = true;
                updateUI(false);

                setTimeout(() => {
                    if (dScore > 21) alert("Dealer Busts! You Win!");
                    else if (dScore > pScore) alert("Dealer Wins.");
                    else if (pScore > dScore) alert("You Win!");
                    else alert("Push (Tie).");
                }, 500);
            }
        </script>
    </body>
    </html>
    """
