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
        <title>YE</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Courier New', Courier, monospace;
                background-color: #121212;
                color: #ffffff;
                text-align: center;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }
            header {
                background-color: #000;
                padding: 20px;
                border-bottom: 2px solid #333;
            }
            h1 {
                margin: 0;
                font-size: 4rem;
                letter-spacing: 10px;
                color: #ffd700; /* Gold */
            }
            .game-container {
                flex-grow: 1;
                background-color: #0b4a22; /* Casino Green */
                padding: 30px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .hand-area {
                margin: 20px 0;
                min-height: 120px;
            }
            .cards {
                font-size: 2rem;
                letter-spacing: 5px;
                background-color: white;
                color: black;
                padding: 15px 25px;
                border-radius: 8px;
                display: inline-block;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
            }
            .status {
                font-size: 1.5rem;
                margin: 15px 0;
                color: #ffcccc;
                min-height: 30px;
            }
            .controls button {
                padding: 15px 30px;
                font-size: 1.2rem;
                margin: 5px;
                cursor: pointer;
                background-color: #222;
                color: white;
                border: 2px solid #555;
                border-radius: 5px;
                transition: 0.2s;
            }
            .controls button:hover {
                background-color: #444;
            }
            .controls button:disabled {
                background-color: #111;
                color: #555;
                cursor: not-allowed;
            }
        </style>
    </head>
    <body>

        <header>
            <h1>YE</h1>
        </header>

        <main class="game-container">
            <h2>BLACKJACK</h2>
            
            <div class="hand-area">
                <h3>Dealer's Hand</h3>
                <div id="dealer-cards" class="cards">?</div>
                <div id="dealer-score">Score: ?</div>
            </div>

            <div class="status" id="game-status">Place your bet and deal!</div>

            <div class="hand-area">
                <h3>Your Hand</h3>
                <div id="player-cards" class="cards">-</div>
                <div id="player-score">Score: 0</div>
            </div>

            <div class="controls">
                <button id="btn-deal" onclick="dealGame()">Deal</button>
                <button id="btn-hit" onclick="hit()" disabled>Hit</button>
                <button id="btn-stand" onclick="stand()" disabled>Stand</button>
            </div>
        </main>

        <script>
            // --- Realistic Blackjack Engine ---
            let deck = [];
            let playerHand = [];
            let dealerHand = [];
            let gameOver = true;

            const suits = ['♠', '♥', '♦', '♣'];
            const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];

            function buildDeck() {
                deck = [];
                // 6 Decks for a realistic house edge
                for (let d = 0; d < 6; d++) {
                    for (let suit of suits) {
                        for (let value of values) {
                            deck.push({ value, suit });
                        }
                    }
                }
                // Shuffle
                for (let i = deck.length - 1; i > 0; i--) {
                    let j = Math.floor(Math.random() * i);
                    let temp = deck[i];
                    deck[i] = deck[j];
                    deck[j] = temp;
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
                    score -= 10; // Convert Ace from 11 to 1
                    aces -= 1;
                }
                return score;
            }

            function updateUI(hideDealerCard = true) {
                const pCards = playerHand.map(c => c.value + c.suit).join('  ');
                document.getElementById('player-cards').innerText = pCards;
                document.getElementById('player-score').innerText = 'Score: ' + calculateScore(playerHand);

                if (hideDealerCard && !gameOver) {
                    const dCards = dealerHand[0].value + dealerHand[0].suit + '  [?]';
                    document.getElementById('dealer-cards').innerText = dCards;
                    document.getElementById('dealer-score').innerText = 'Score: ?';
                } else {
                    const dCards = dealerHand.map(c => c.value + c.suit).join('  ');
                    document.getElementById('dealer-cards').innerText = dCards;
                    document.getElementById('dealer-score').innerText = 'Score: ' + calculateScore(dealerHand);
                }

                document.getElementById('btn-deal').disabled = !gameOver;
                document.getElementById('btn-hit').disabled = gameOver;
                document.getElementById('btn-stand').disabled = gameOver;
            }

            function dealGame() {
                buildDeck();
                playerHand = [deck.pop(), deck.pop()];
                dealerHand = [deck.pop(), deck.pop()];
                gameOver = false;
                document.getElementById('game-status').innerText = 'Hit or Stand?';
                
                // Check for immediate Blackjack
                if (calculateScore(playerHand) === 21) {
                    endGame("BLACKJACK! You Win!");
                } else {
                    updateUI(true);
                }
            }

            function hit() {
                playerHand.push(deck.pop());
                if (calculateScore(playerHand) > 21) {
                    endGame("Bust! Dealer Wins.");
                } else {
                    updateUI(true);
                }
            }

            function stand() {
                // Dealer logic: hit until 17
                while (calculateScore(dealerHand) < 17) {
                    dealerHand.push(deck.pop());
                }
                
                let pScore = calculateScore(playerHand);
                let dScore = calculateScore(dealerHand);

                if (dScore > 21) {
                    endGame("Dealer Busts! You Win!");
                } else if (dScore > pScore) {
                    endGame("Dealer Wins.");
                } else if (pScore > dScore) {
                    endGame("You Win!");
                } else {
                    endGame("Push (Tie).");
                }
            }

            function endGame(message) {
                gameOver = true;
                document.getElementById('game-status').innerText = message;
                updateUI(false); // Reveal dealer's full hand
            }
        </script>
    </body>
    </html>
    """
