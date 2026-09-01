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
                --btn-primary-hover: #4295fa;
                --text-main: #ffffff;
                --text-muted: #b1bad3;
                --card-red: #e9113c;
                --card-black: #0f212e;
                --badge-win: #00e701;
                --badge-bust: #e9113c;
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
                letter-spacing: 1px;
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
            }

            .hand-section {
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
                width: 100%;
            }

            .hands-split-wrapper {
                display: flex;
                justify-content: center;
                gap: 20px;
                width: 100%;
            }

            .single-hand {
                display: flex;
                flex-direction: column;
                align-items: center;
                transition: transform 0.2s;
            }
            .single-hand.active-hand {
                transform: scale(1.05);
            }
            .single-hand.active-hand .score-bubble {
                box-shadow: 0 0 10px #1475e1;
            }

            .score-bubble {
                background: #2f4553;
                color: #fff;
                padding: 4px 14px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 800;
                margin-bottom: 8px;
                transition: all 0.3s ease;
            }

            .cards-container {
                display: flex;
                justify-content: center;
                min-height: 105px;
            }

            /* Card Styling & Dealing Animation */
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
                animation: dealSlide 0.35s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
            }
            .card:not(:first-child) {
                margin-left: -32px;
            }

            @keyframes dealSlide {
                from {
                    transform: translateY(-80px) scale(0.6) rotate(-10deg);
                    opacity: 0;
                }
                to {
                    transform: translateY(0) scale(1) rotate(0deg);
                    opacity: 1;
                }
            }

            .card.red { color: var(--card-red); }
            .card.black { color: var(--card-black); }

            .card-corner {
                font-size: 14px;
                line-height: 1;
            }
            .card-center {
                font-size: 22px;
                align-self: center;
            }

            .card.back {
                background: #1475e1;
                background-image: repeating-linear-gradient(45deg, #1062be 0, #1062be 5px, #1475e1 5px, #1475e1 10px);
                border: 2px solid #ffffff;
            }

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
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                box-shadow: 0 -4px 15px rgba(0,0,0,0.3);
            }

            .btn-main-bet {
                width: 100%;
                background: #00e701;
                color: #011d01;
                border: none;
                padding: 16px;
                border-radius: 8px;
                font-size: 17px;
                font-weight: 800;
                cursor: pointer;
                margin-bottom: 12px;
                transition: opacity 0.2s;
            }
            .btn-main-bet:disabled {
                opacity: 0.4;
                cursor: not-allowed;
            }

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
                border: 2px solid #2f4553;
                padding: 10px 14px;
                border-radius: 8px;
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
                cursor: pointer;
                font-weight: bold;
            }

            .actions-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }

            .action-btn {
                background: var(--bg-card);
                color: #ffffff;
                border: none;
                padding: 14px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.2s;
            }
            .action-btn:hover:not(:disabled) {
                background: #2f4553;
            }
            .action-btn:disabled {
                opacity: 0.35;
                cursor: not-allowed;
            }
        </style>
    </head>
    <body>

        <header>
            <div class="logo">YE</div>
            <div class="wallet-badge">
                <span id="display-balance">$100.00</span> 🪙
            </div>
            <div style="display:flex; gap:10px; align-items:center;">
                <button class="btn-wallet">Deposit</button>
            </div>
        </header>

        <main class="game-table">
            <!-- Dealer -->
            <div class="hand-section">
                <div class="score-bubble" id="dealer-score">-</div>
                <div class="cards-container" id="dealer-cards"></div>
            </div>

            <div class="rule-banner">
                BLACKJACK PAYS 3 TO 2<br>
                DEALER STANDS ON 17
            </div>

            <!-- Player (Supports Split Hands) -->
            <div class="hand-section">
                <div class="hands-split-wrapper" id="player-hands-wrapper">
                    <div class="single-hand active-hand" id="hand-0">
                        <div class="score-bubble" id="player-score-0">-</div>
                        <div class="cards-container" id="player-cards-0"></div>
                    </div>
                </div>
            </div>
        </main>

        <section class="controls-panel">
            <button class="btn-main-bet" id="btn-bet" onclick="dealHand()">Bet</button>

            <div class="bet-row">
                <span>Bet Amount</span>
                <span id="bet-crypto-label">10.00 USD</span>
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
                <button class="action-btn" id="btn-split" onclick="splitAction()" disabled>Split 🎴</button>
                <button class="action-btn" id="btn-double" onclick="doubleAction()" disabled>Double 2×</button>
            </div>
        </section>

        <script>
            let balance = 100.00;
            let currentBet = 10.00;
            let deck = [];
            let dealerHand = [];
            let playerHands = []; // Array of hands to support splitting
            let activeHandIdx = 0;
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
                document.getElementById('bet-crypto-label').innerText = `${currentBet.toFixed(2)} USD`;
            }

            function dealHand() {
                if (balance < currentBet) {
                    alert("Insufficient balance!");
                    return;
                }
                balance -= currentBet;
                updateBalance();

                buildDeck();
                dealerHand = [deck.pop(), deck.pop()];
                playerHands = [[deck.pop(), deck.pop()]];
                activeHandIdx = 0;
                gameOver = false;

                renderTable(true);
                checkInitialState();
            }

            function checkInitialState() {
                let hand = playerHands[0];
                let pScore = calculateScore(hand);

                // Enable Split if matching ranks
                const canSplit = getCardValue(hand[0]) === getCardValue(hand[1]) && balance >= currentBet;
                document.getElementById('btn-split').disabled = !canSplit;
                document.getElementById('btn-double').disabled = balance < currentBet;

                if (pScore === 21) {
                    resolveDealerTurn();
                }
            }

            function hitAction() {
                let hand = playerHands[activeHandIdx];
                hand.push(deck.pop());
                document.getElementById('btn-split').disabled = true;
                document.getElementById('btn-double').disabled = true;

                let score = calculateScore(hand);
                if (score >= 21) {
                    standAction();
                } else {
                    renderTable(true);
                }
            }

            function doubleAction() {
                if (balance < currentBet) return;
                balance -= currentBet;
                updateBalance();

                let hand = playerHands[activeHandIdx];
                hand.push(deck.pop());
                renderTable(true);
                standAction();
            }

            function splitAction() {
                if (balance < currentBet) return;
                balance -= currentBet;
                updateBalance();

                let hand = playerHands[0];
                playerHands = [
                    [hand[0], deck.pop()],
                    [hand[1], deck.pop()]
                ];
                activeHandIdx = 0;

                renderTable(true);
                document.getElementById('btn-split').disabled = true;
            }

            function standAction() {
                if (activeHandIdx < playerHands.length - 1) {
                    activeHandIdx++;
                    renderTable(true);
                } else {
                    resolveDealerTurn();
                }
            }

            function resolveDealerTurn() {
                gameOver = true;
                while (calculateScore(dealerHand) < 17) {
                    dealerHand.push(deck.pop());
                }
                renderTable(false);
                calculatePayouts();
            }

            function calculatePayouts() {
                let dScore = calculateScore(dealerHand);

                playerHands.forEach((hand) => {
                    let pScore = calculateScore(hand);
                    if (pScore > 21) {
                        // Bust
                    } else if (dScore > 21 || pScore > dScore) {
                        balance += (pScore === 21 && hand.length === 2) ? currentBet * 2.5 : currentBet * 2;
                    } else if (pScore === dScore) {
                        balance += currentBet; // Push
                    }
                });

                updateBalance();
                updateControls();
            }

            function renderTable(hideHoleCard) {
                // Dealer
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

                // Player Hands
                const wrapper = document.getElementById('player-hands-wrapper');
                wrapper.innerHTML = playerHands.map((hand, idx) => {
                    let score = calculateScore(hand);
                    let scoreText = score > 21 ? `BUST (${score})` : score;
                    let isActive = (idx === activeHandIdx && !gameOver) ? 'active-hand' : '';
                    return `
                        <div class="single-hand ${isActive}" id="hand-${idx}">
                            <div class="score-bubble">${scoreText}</div>
                            <div class="cards-container">${hand.map(c => renderCard(c)).join('')}</div>
                        </div>`;
                }).join('');

                updateControls();
            }

            function updateControls() {
                document.getElementById('btn-bet').disabled = !gameOver;
                document.getElementById('btn-hit').disabled = gameOver;
                document.getElementById('btn-stand').disabled = gameOver;
                if (gameOver) {
                    document.getElementById('btn-split').disabled = true;
                    document.getElementById('btn-double').disabled = true;
                }
            }

            function updateBalance() {
                document.getElementById('display-balance').innerText = `$${balance.toFixed(2)}`;
            }
        </script>
    </body>
    </html>
    """
