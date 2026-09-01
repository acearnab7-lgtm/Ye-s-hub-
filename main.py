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
        <title>YE Casino - Blackjack</title>
        <style>
            :root {
                --bg-main: #0f212e;
                --bg-secondary: #1a2c38;
                --bg-card: #213743;
                --accent-blue: #00e701;
                --btn-primary: #1475e1;
                --text-main: #ffffff;
                --text-muted: #b1bad3;
                --card-red: #e9113c;
                --card-black: #0f212e;
            }

            * {
                box-sizing: border-box;
                user-select: none;
            }

            body {
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: var(--bg-main);
                color: var(--text-main);
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                overflow-x: hidden;
            }

            /* Header */
            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: var(--bg-secondary);
                padding: 10px 16px;
                border-bottom: 2px solid #213743;
            }
            .logo {
                font-size: 26px;
                font-weight: 900;
                font-style: italic;
                color: #fff;
            }
            .wallet-badge {
                display: flex;
                align-items: center;
                gap: 8px;
                background: var(--bg-main);
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            .btn-wallet {
                background: var(--btn-primary);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
            }

            /* Table Layout */
            .game-table {
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                justify-content: space-around;
                align-items: center;
                padding: 15px 10px;
                min-height: 380px;
                position: relative;
            }

            /* The Shoe Icon */
            .deck-shoe {
                position: absolute;
                top: 15px;
                right: 20px;
                font-size: 24px;
                background: #ffffff;
                border-radius: 4px;
                width: 32px;
                height: 20px;
                box-shadow: 0 3px 0 #b1bad3, 0 6px 0 #ffffff;
            }

            .hand-section {
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
            }

            .score-bubble {
                background: #2f4553;
                color: #fff;
                padding: 4px 14px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 800;
                margin-bottom: 8px;
            }

            .cards-container {
                display: flex;
                justify-content: center;
                min-height: 105px;
            }

            /* SLOW Card Styling & Dealing Animation */
            .card {
                width: 65px;
                height: 95px;
                background: #ffffff;
                border-radius: 8px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                padding: 6px;
                font-weight: 800;
                box-shadow: -4px 4px 10px rgba(0,0,0,0.4);
                position: relative;
                
                /* Changed to a slower, smoother drop */
                opacity: 0;
                animation: dealSlide 0.7s cubic-bezier(0.1, 0.9, 0.2, 1) forwards;
            }
            
            /* Stagger the animations so they deal one by one */
            .card:nth-child(1) { animation-delay: 0.1s; }
            .card:nth-child(2) { animation-delay: 0.6s; }
            .card:nth-child(3) { animation-delay: 0.1s; } /* For hits */
            .card:nth-child(4) { animation-delay: 0.1s; }
            
            .card:not(:first-child) {
                margin-left: -32px;
            }

            @keyframes dealSlide {
                from {
                    transform: translateY(-120px) scale(0.8);
                    opacity: 0;
                }
                to {
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }
            }

            .card.red { color: var(--card-red); }
            .card.black { color: var(--card-black); }
            .card.back {
                background: #1475e1;
                background-image: repeating-linear-gradient(45deg, #1062be 0, #1062be 5px, #1475e1 5px, #1475e1 10px);
                border: 2px solid #ffffff;
            }
            .card-corner { font-size: 14px; line-height: 1; }
            .card-center { font-size: 22px; align-self: center; }

            .rule-banner {
                color: #2f4553;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1.5px;
                text-align: center;
                line-height: 1.6;
            }

            /* Bottom Controls */
            .controls-panel {
                background: var(--bg-secondary);
                padding: 16px;
            }

            .btn-main-bet {
                width: 100%;
                background: var(--btn-primary);
                color: #ffffff;
                border: none;
                padding: 14px;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin-bottom: 12px;
            }
            .btn-main-bet:disabled { opacity: 0.4; }

            .bet-row {
                display: flex;
                justify-content: space-between;
                font-size: 12px;
                color: var(--text-muted);
                margin-bottom: 6px;
                font-weight: 600;
            }

            .bet-input-box {
                background: var(--bg-main);
                padding: 10px 14px;
                border-radius: 4px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
                font-weight: 700;
            }

            .bet-modifiers button {
                background: var(--bg-card);
                border: none;
                color: var(--text-muted);
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: bold;
            }

            .actions-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 20px;
            }

            .action-btn {
                background: var(--bg-card);
                color: #ffffff;
                border: none;
                padding: 14px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 700;
            }
            .action-btn:disabled { opacity: 0.35; }

            /* New Extra UI Elements */
            .extra-actions-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }
            .icon-btns {
                display: flex;
                gap: 10px;
            }
            .icon-circle {
                background: var(--bg-main);
                width: 38px;
                height: 38px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                color: var(--text-muted);
                font-size: 18px;
            }
            .btn-fairness {
                background: var(--bg-card);
                color: var(--text-main);
                border: none;
                padding: 10px 16px;
                border-radius: 20px;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .originals-banner {
                background: var(--bg-card);
                border-radius: 8px;
                padding: 12px;
                display: flex;
                align-items: center;
                margin-bottom: 15px;
            }
            .orig-logo {
                background: #2f4553;
                width: 40px;
                height: 40px;
                border-radius: 6px;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
                font-style: italic;
                margin-right: 12px;
            }
            .orig-text {
                flex-grow: 1;
                font-weight: bold;
                line-height: 1.3;
            }
            .orig-text small {
                color: var(--text-muted);
                font-weight: normal;
                font-size: 12px;
            }
            .orig-heart {
                background: var(--bg-main);
                padding: 10px;
                border-radius: 6px;
                color: var(--text-muted);
            }

            .save-game-row {
                background: var(--bg-card);
                border-radius: 8px;
                padding: 16px 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .save-badge {
                background: #2f4553;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                margin-left: 8px;
                color: var(--text-muted);
            }
            .save-arrow {
                color: var(--text-muted);
                font-size: 18px;
            }

            /* Bottom Nav Dummy */
            .bottom-nav {
                display: flex;
                justify-content: space-around;
                padding: 15px 0;
                background: var(--bg-main);
                font-size: 11px;
                color: var(--text-muted);
                border-top: 1px solid #213743;
            }
            .nav-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 4px;
            }
            .nav-item.active {
                color: white;
            }
        </style>
    </head>
    <body>

        <header>
            <div class="logo">YE</div>
            <div class="wallet-badge">
                <span id="display-balance">$100.00</span> 🪙
            </div>
            <div>
                <button class="btn-wallet">Wallet</button>
            </div>
        </header>

        <main class="game-table">
            <div class="deck-shoe"></div>

            <div class="hand-section">
                <div class="score-bubble" id="dealer-score">-</div>
                <div class="cards-container" id="dealer-cards"></div>
            </div>

            <div class="rule-banner">
                BLACKJACK PAYS 3 TO 2<br>
                INSURANCE PAYS 2 TO 1
            </div>

            <div class="hand-section">
                <div class="score-bubble" id="player-score">-</div>
                <div class="cards-container" id="player-cards"></div>
            </div>
        </main>

        <section class="controls-panel">
            <button class="btn-main-bet" id="btn-bet" onclick="dealHand()">Bet</button>

            <div class="bet-row">
                <span>Bet Amount</span>
                <span id="bet-crypto-label">10.00000000 USDC</span>
            </div>

            <div class="bet-input-box">
                <span id="bet-display">$ 10.00</span>
                <div class="bet-modifiers">
                    <button onclick="adjustBet(0.5)">½</button>
                    <button onclick="adjustBet(2)">2×</button>
                </div>
            </div>

            <div class="actions-grid">
                <button class="action-btn" id="btn-hit" onclick="hitAction()" disabled>Hit 🗂️</button>
                <button class="action-btn" id="btn-stand" onclick="standAction()" disabled>Stand ✋</button>
                <button class="action-btn" id="btn-split" disabled>Split 🎴</button>
                <button class="action-btn" id="btn-double" disabled>Double 2×</button>
            </div>

            <!-- New Bottom UI Sections -->
            <div class="extra-actions-row">
                <div class="icon-btns">
                    <div class="icon-circle">⚙️</div>
                    <div class="icon-circle">📈</div>
                </div>
                <button class="btn-fairness">✔️ Fairness</button>
            </div>

            <div class="originals-banner">
                <div class="orig-logo">YE</div>
                <div class="orig-text">
                    YE Originals<br>
                    <small>181.17K Followers</small>
                </div>
                <div class="orig-heart">♡</div>
            </div>

            <div class="save-game-row">
                <div>Blackjack <span class="save-badge">Save Game</span></div>
                <div class="save-arrow">›</div>
            </div>
        </section>

        <nav class="bottom-nav">
            <div class="nav-item">🔍 Browse</div>
            <div class="nav-item active">🎰 Casino</div>
            <div class="nav-item">⭐ For You</div>
            <div class="nav-item">⚽ Sports</div>
            <div class="nav-item">💬 Chat</div>
        </nav>

        <script>
            // Card sliding sound effect
            const dealSound = new Audio('https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3');

            let balance = 100.00;
            let currentBet = 10.00;
            let deck = [];
            let dealerHand = [];
            let playerHand = [];
            let gameOver = true;

            const suits = { '♠': 'black', '♥': 'red', '♦': 'red', '♣': 'black' };
            const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];

            function playSound(times, interval) {
                let count = 0;
                let soundInterval = setInterval(() => {
                    let s = dealSound.cloneNode();
                    s.volume = 0.5;
                    s.play();
                    count++;
                    if (count >= times) clearInterval(soundInterval);
                }, interval);
            }

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
                    let j = Math.floor(Math.random() * (i + 1));
                    [deck[i], deck[j]] = [deck[j], deck[i]];
                }
            }

            function getCardValue(card) {
                if (['J', 'Q', 'K'].includes(card.value)) return 10;
                if (card.value === 'A') return 11;
                return parseInt(card.value);
            }

            function calculateScore(hand) {
                let score = 0, aces = 0;
                for (let c of hand) {
                    score += getCardValue(c);
                    if (c.value === 'A') aces++;
                }
                while (score > 21 && aces > 0) {
                    score -= 10;
                    aces--;
                }
                return score;
            }

            function renderCard(card, isBack = false) {
                if (isBack) return `<div class="card back"></div>`;
                return `
                    <div class="card ${card.color}">
                        <div class="card-corner">${card.value}<br>${card.suit}</div>
                        <div class="card-center">${card.suit}</div>
                        <div class="card-corner" style="transform: rotate(180deg);">${card.value}<br>${card.suit}</div>
                    </div>`;
            }

            function adjustBet(multiplier) {
                if (!gameOver) return;
                currentBet = Math.max(1, Math.min(balance, currentBet * multiplier));
                document.getElementById('bet-display').innerText = `$ ${currentBet.toFixed(2)}`;
            }

            function dealHand() {
                if (balance < currentBet) return;
                balance -= currentBet;
                updateBalance();

                buildDeck();
                dealerHand = [deck.pop(), deck.pop()];
                playerHand = [deck.pop(), deck.pop()];
                gameOver = false;
                
                // Play sound twice for initial deal (staggered)
                playSound(4, 300);

                renderTable(true);
                
                if (calculateScore(playerHand) === 21) {
                    setTimeout(resolveDealerTurn, 1500); // Wait for animation
                }
            }

            function hitAction() {
                playerHand.push(deck.pop());
                playSound(1, 0); // Play single deal sound

                let score = calculateScore(playerHand);
                renderTable(true);
                if (score >= 21) {
                    setTimeout(standAction, 1000);
                }
            }

            function standAction() {
                resolveDealerTurn();
            }

            function resolveDealerTurn() {
                gameOver = true;
                
                let drawInterval = setInterval(() => {
                    if (calculateScore(dealerHand) < 17) {
                        dealerHand.push(deck.pop());
                        playSound(1, 0);
                        renderTable(false);
                    } else {
                        clearInterval(drawInterval);
                        calculatePayouts();
                    }
                }, 800);
                
                if (calculateScore(dealerHand) >= 17) {
                    renderTable(false);
                    calculatePayouts();
                }
            }

            function calculatePayouts() {
                let dScore = calculateScore(dealerHand);
                let pScore = calculateScore(playerHand);
                
                if (pScore <= 21) {
                    if (dScore > 21 || pScore > dScore) {
                        balance += (pScore === 21 && playerHand.length === 2) ? currentBet * 2.5 : currentBet * 2;
                    } else if (pScore === dScore) {
                        balance += currentBet;
                    }
                }
                
                updateBalance();
                updateControls();
            }

            function renderTable(hideHoleCard) {
                const dCardsElem = document.getElementById('dealer-cards');
                const dScoreElem = document.getElementById('dealer-score');

                if (hideHoleCard) {
                    dCardsElem.innerHTML = renderCard(dealerHand[0]) + renderCard(dealerHand[1], true);
                    dScoreElem.innerText = getCardValue(dealerHand[0]);
                } else {
                    dCardsElem.innerHTML = dealerHand.map(c => renderCard(c)).join('');
                    let finalDScore = calculateScore(dealerHand);
                    dScoreElem.innerText = finalDScore > 21 ? `BUST (${finalDScore})` : finalDScore;
                }

                document.getElementById('player-cards').innerHTML = playerHand.map(c => renderCard(c)).join('');
                let pScore = calculateScore(playerHand);
                document.getElementById('player-score').innerText = pScore > 21 ? `BUST (${pScore})` : pScore;
                
                updateControls();
            }

            function updateControls() {
                document.getElementById('btn-bet').disabled = !gameOver;
                document.getElementById('btn-hit').disabled = gameOver;
                document.getElementById('btn-stand').disabled = gameOver;
            }

            function updateBalance() {
                document.getElementById('display-balance').innerText = `$${balance.toFixed(2)}`;
            }
        </script>
    </body>
    </html>
    """
