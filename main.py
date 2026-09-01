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
        <title>Kanye Casino</title>
        <style>
            :root {
                --bg-main: #0f212e; --bg-secondary: #1a2c38; --bg-card: #213743;
                --accent-yellow: #ffb703; --btn-primary: #1475e1;
                --text-main: #ffffff; --text-muted: #b1bad3;
                --card-red: #e9113c; --card-black: #0f212e;
            }
            * { box-sizing: border-box; user-select: none; }
            body { margin: 0; padding: 0; font-family: -apple-system, sans-serif; background: var(--bg-main); color: var(--text-main); display: flex; flex-direction: column; min-height: 100vh; overflow-x: hidden; }
            
            /* Header */
            header { display: flex; justify-content: space-between; align-items: center; background: var(--bg-secondary); padding: 10px 16px; border-bottom: 2px solid #213743; }
            .logo { font-size: 24px; font-weight: 900; font-style: italic; color: var(--accent-yellow); letter-spacing: 1px; }
            .wallet-area { display: flex; align-items: center; gap: 10px; background: var(--bg-main); padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; border: 1px solid #2f4553; }
            .wallet-add { background: var(--accent-yellow); color: #000; border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; }
            
            /* Views Management */
            .view { display: none; flex-grow: 1; flex-direction: column; }
            .view.active { display: flex; }

            /* --- LOBBY VIEW --- */
            .lobby-container { padding: 15px; overflow-y: auto; flex-grow: 1; padding-bottom: 80px; }
            .promo-banner {
                background: linear-gradient(135deg, #2b1055, #7597de);
                border-radius: 12px; padding: 20px; position: relative; margin-bottom: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4); overflow: hidden;
            }
            .promo-banner h2 { margin: 0 0 10px 0; font-size: 22px; font-weight: 900; }
            .btn-learn { background: var(--accent-yellow); color: #000; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; }
            
            .game-grid-card {
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                border-radius: 12px; padding: 20px; margin-bottom: 15px; cursor: pointer;
                display: flex; justify-content: space-between; align-items: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: transform 0.1s;
            }
            .game-grid-card:active { transform: scale(0.98); }
            .game-grid-card h3 { margin: 0 0 5px 0; font-size: 20px; }
            .game-grid-card p { margin: 0; color: var(--text-muted); font-size: 13px; }
            .game-icon-preview { font-size: 32px; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 10px; }

            /* --- BLACKJACK VIEW --- */
            .game-table { flex-grow: 1; display: flex; flex-direction: column; justify-content: space-around; align-items: center; padding: 15px 10px; min-height: 340px; position: relative; }
            .bust-meme { display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 260px; border-radius: 12px; pointer-events: none; z-index: 50; opacity: 0.25; mix-blend-mode: screen; filter: contrast(1.4) saturate(1.2) drop-shadow(0 0 15px rgba(255,255,255,0.3)); }

            .insurance-overlay { display: none; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 33, 46, 0.85); z-index: 100; flex-direction: column; justify-content: center; align-items: center; backdrop-filter: blur(4px); }
            .insurance-box { background: var(--bg-secondary); border: 2px solid var(--bg-card); padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
            .insurance-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
            .insurance-subtitle { color: var(--text-muted); font-size: 12px; margin-bottom: 20px; }
            .insurance-btns { display: flex; gap: 10px; justify-content: center; }
            .ins-btn { padding: 12px 20px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px; }
            .ins-yes { background: #00e701; color: #011d01; } .ins-no { background: var(--bg-card); color: white; }
            .ins-yes:disabled { opacity: 0.4; cursor: not-allowed; }

            .deck-shoe { position: absolute; top: 15px; right: 20px; font-size: 24px; background: #ffffff; border-radius: 4px; width: 32px; height: 20px; box-shadow: 0 3px 0 #b1bad3, 0 6px 0 #ffffff; }
            .hand-section { display: flex; flex-direction: column; align-items: center; width: 100%; }
            .hands-split-wrapper { display: flex; justify-content: center; gap: 15px; width: 100%; }
            .single-hand { display: flex; flex-direction: column; align-items: center; transition: transform 0.2s; }
            .single-hand.active-hand { transform: scale(1.05); }
            .single-hand.active-hand .score-bubble { box-shadow: 0 0 10px #1475e1; }

            .score-bubble { background: #2f4553; color: #fff; padding: 4px 14px; border-radius: 12px; font-size: 13px; font-weight: 800; margin-bottom: 8px; }
            .cards-container { display: flex; justify-content: center; min-height: 105px; }
            
            .card { width: 65px; height: 95px; background: #ffffff; border-radius: 8px; display: flex; flex-direction: column; justify-content: space-between; padding: 6px; font-weight: 800; box-shadow: -4px 4px 10px rgba(0,0,0,0.4); position: relative; opacity: 0; animation: dealSlide 0.7s cubic-bezier(0.1, 0.9, 0.2, 1) forwards; }
            .card:nth-child(1) { animation-delay: 0.1s; } .card:nth-child(2) { animation-delay: 0.6s; } .card:nth-child(3) { animation-delay: 0.1s; } .card:nth-child(4) { animation-delay: 0.1s; }
            .card:not(:first-child) { margin-left: -32px; }
            @keyframes dealSlide { from { transform: translateY(-120px) scale(0.8); opacity: 0; } to { transform: translateY(0) scale(1); opacity: 1; } }
            .card.red { color: var(--card-red); } .card.black { color: var(--card-black); }
            .card.back { background: #1475e1; background-image: repeating-linear-gradient(45deg, #1062be 0, #1062be 5px, #1475e1 5px, #1475e1 10px); border: 2px solid #ffffff; }
            .card-corner { font-size: 14px; line-height: 1; } .card-center { font-size: 22px; align-self: center; }
            .rule-banner { color: #2f4553; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; text-align: center; line-height: 1.6; }
            
            .controls-panel { background: var(--bg-secondary); padding: 14px; }
            .btn-main-bet { width: 100%; background: var(--btn-primary); color: #ffffff; border: none; padding: 14px; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin-bottom: 10px; }
            .btn-main-bet:disabled { opacity: 0.4; }
            .bet-row { display: flex; justify-content: space-between; font-size: 12px; color: var(--text-muted); margin-bottom: 4px; font-weight: 600; }
            .bet-input-box { background: var(--bg-main); padding: 8px 12px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: 700; }
            .bet-modifiers button { background: var(--bg-card); border: none; color: var(--text-muted); padding: 4px 8px; border-radius: 4px; font-weight: bold; cursor: pointer; }
            .actions-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
            .action-btn { background: var(--bg-card); color: #ffffff; border: none; padding: 12px; border-radius: 4px; font-size: 14px; font-weight: 700; cursor: pointer; }
            .action-btn:disabled { opacity: 0.35; cursor: not-allowed; }
            .back-to-lobby { background: var(--bg-card); color: var(--text-muted); border: none; padding: 8px; width: 100%; border-radius: 4px; font-weight: bold; cursor: pointer; margin-top: 5px; }

            /* Bottom Navigation Bar */
            .bottom-nav { display: flex; justify-content: space-around; padding: 10px 0; background: var(--bg-secondary); font-size: 11px; color: var(--text-muted); border-top: 1px solid #213743; position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000; }
            .nav-item { display: flex; flex-direction: column; align-items: center; gap: 3px; cursor: pointer; }
            .nav-item.active { color: var(--accent-yellow); }
        </style>
    </head>
    <body>

        <header>
            <div class="logo">KANYE</div>
            <div class="wallet-area">
                <span id="display-balance">$100.00</span> 🪙
                <div class="wallet-add">+</div>
            </div>
        </header>

        <!-- VIEW 1: CASINO LOBBY -->
        <div id="lobby-view" class="view active lobby-container">
            <div class="promo-banner">
                <h2>$100,000 Weekly Raffle</h2>
                <button class="btn-learn" onclick="switchView('game')">Play Now</button>
            </div>
            
            <div style="font-weight: bold; margin-bottom: 10px; color: var(--text-muted);">Featured Games</div>
            
            <div class="game-grid-card" onclick="switchView('game')">
                <div>
                    <h3>Blackjack</h3>
                    <p>Classic 6-Deck Vegas Rules</p>
                </div>
                <div class="game-icon-preview">🃏</div>
            </div>

            <div class="game-grid-card" onclick="alert('Coming soon!')">
                <div>
                    <h3>Roulette</h3>
                    <p>European & American Tables</p>
                </div>
                <div class="game-icon-preview">🎡</div>
            </div>

            <div class="game-grid-card" onclick="alert('Coming soon!')">
                <div>
                    <h3>Slots</h3>
                    <p>Thousands of Crypto Slots</p>
                </div>
                <div class="game-icon-preview">🎰</div>
            </div>
        </div>

        <!-- VIEW 2: BLACKJACK GAME INTERFACE -->
        <div id="game-view" class="view">
            <main class="game-table">
                <div class="deck-shoe"></div>
                
                <video id="meme-video" class="bust-meme" src="https://files.catbox.moe/q89owi.mp4" playsinline></video>

                <div class="insurance-overlay" id="insurance-prompt">
                    <div class="insurance-box">
                        <div class="insurance-title">Dealer shows an Ace</div>
                        <div class="insurance-subtitle">Insurance pays 2:1 if Dealer has Blackjack</div>
                        <div class="insurance-btns">
                            <button class="ins-btn ins-yes" id="btn-buy-ins" onclick="resolveInsurance(true)">Buy</button>
                            <button class="ins-btn ins-no" onclick="resolveInsurance(false)">Decline</button>
                        </div>
                    </div>
                </div>

                <div class="hand-section">
                    <div class="score-bubble" id="dealer-score">-</div>
                    <div class="cards-container" id="dealer-cards"></div>
                </div>
                
                <div class="rule-banner">BLACKJACK PAYS 3 TO 2<br>INSURANCE PAYS 2 TO 1</div>
                
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
                <div class="bet-row"><span>Bet Amount</span><span id="bet-crypto-label">10.00000000 USDC</span></div>
                <div class="bet-input-box">
                    <span id="bet-display">$ 10.00</span>
                    <div class="bet-modifiers">
                        <button onclick="adjustBet(0.5)">½</button><button onclick="adjustBet(2)">2×</button>
                    </div>
                </div>
                <div class="actions-grid">
                    <button class="action-btn" id="btn-hit" onclick="hitAction()" disabled>Hit 🗂️</button>
                    <button class="action-btn" id="btn-stand" onclick="standAction()" disabled>Stand ✋</button>
                    <button class="action-btn" id="btn-split" disabled>Split 🎴</button>
                    <button class="action-btn" id="btn-double" disabled>Double 2×</button>
                </div>
                <button class="back-to-lobby" onclick="switchView('lobby')">← Back to Casino Lobby</button>
            </section>
        </div>

        <!-- Bottom Navigation Bar -->
        <nav class="bottom-nav">
            <div class="nav-item" onclick="switchView('lobby')"><span>🔍</span> Browse</div>
            <div class="nav-item active" onclick="switchView('lobby')"><span>🎰</span> Casino</div>
            <div class="nav-item" onclick="switchView('game')"><span>🃏</span> Blackjack</div>
            <div class="nav-item" onclick="alert('Chat coming soon!')"><span>💬</span> Chat</div>
        </nav>

        <script>
            const dealSound = new Audio('https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3');
            const memeVideo = document.getElementById('meme-video');

            let balance = 100.00; 
            let currentBet = 10.00; 
            let insuranceBet = 0;
            let deck = []; 
            let dealerHand = []; 
            let playerHands = [];
            let handBets = [];
            let activeHandIdx = 0; 
            let gameOver = true; 
            let waitingForInsurance = false;

            const suits = { '♠': 'black', '♥': 'red', '♦': 'red', '♣': 'black' };
            const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];

            function switchView(viewName) {
                document.getElementById('lobby-view').classList.remove('active');
                document.getElementById('game-view').classList.remove('active');
                if (viewName === 'lobby') {
                    document.getElementById('lobby-view').classList.add('active');
                } else {
                    document.getElementById('game-view').classList.add('active');
                }
            }

            function playSound(times, interval) {
                let count = 0;
                let soundInterval = setInterval(() => {
                    let s = dealSound.cloneNode(); s.volume = 0.5; s.play();
                    count++; if (count >= times) clearInterval(soundInterval);
                }, interval);
            }

            function buildDeck() {
                deck = [];
                for (let d = 0; d < 6; d++) {
                    for (let [suit, color] of Object.entries(suits)) {
                        for (let value of values) { deck.push({ value, suit, color }); }
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
                for (let c of hand) { score += getCardValue(c); if (c.value === 'A') aces++; }
                while (score > 21 && aces > 0) { score -= 10; aces--; }
                return score;
            }

            function renderCard(card, isBack = false) {
                if (isBack) return `<div class="card back"></div>`;
                return `<div class="card ${card.color}"><div class="card-corner">${card.value}<br>${card.suit}</div><div class="card-center">${card.suit}</div><div class="card-corner" style="transform: rotate(180deg);">${card.value}<br>${card.suit}</div></div>`;
            }

            function adjustBet(multiplier) {
                if (!gameOver) return;
                currentBet = Math.max(1, Math.min(balance, currentBet * multiplier));
                document.getElementById('bet-display').innerText = `$ ${currentBet.toFixed(2)}`;
            }

            function dealHand() {
                if (balance < currentBet) return;
                balance -= currentBet; 
                insuranceBet = 0; 
                updateBalance();
                
                memeVideo.style.display = 'none';
                memeVideo.pause();
                memeVideo.currentTime = 0;

                buildDeck(); 
                dealerHand = [deck.pop(), deck.pop()]; 
                playerHands = [[deck.pop(), deck.pop()]];
                handBets = [currentBet];
                activeHandIdx = 0;
                gameOver = false; 
                waitingForInsurance = false;
                
                playSound(4, 300); 
                renderTable(true);
                
                setTimeout(() => {
                    if (dealerHand[0].value === 'A') promptInsurance();
                    else checkInitialState();
                }, 1300);
            }

            function promptInsurance() {
                waitingForInsurance = true;
                const insCost = currentBet / 2;
                const buyBtn = document.getElementById('btn-buy-ins');
                buyBtn.innerText = `Buy ($${insCost.toFixed(2)})`;
                buyBtn.disabled = balance < insCost;
                document.getElementById('insurance-prompt').style.display = 'flex';
                updateControls();
            }

            function resolveInsurance(buy) {
                document.getElementById('insurance-prompt').style.display = 'none';
                waitingForInsurance = false;
                
                if (buy) {
                    const insCost = currentBet / 2;
                    if (balance >= insCost) { balance -= insCost; insuranceBet = insCost; updateBalance(); }
                }

                if (calculateScore(dealerHand) === 21) {
                    renderTable(false);
                    if (insuranceBet > 0) { balance += insuranceBet * 3; setTimeout(() => alert("Dealer has Blackjack. Insurance pays!"), 500); } 
                    else { setTimeout(() => alert("Dealer has Blackjack!"), 500); }
                    if (calculateScore(playerHands[0]) === 21) balance += handBets[0];
                    gameOver = true; updateBalance(); updateControls();
                } else {
                    if (insuranceBet > 0) setTimeout(() => alert("Dealer doesn't have Blackjack. Insurance lost."), 300);
                    checkInitialState();
                }
            }

            function checkInitialState() {
                let hand = playerHands[activeHandIdx];
                let pScore = calculateScore(hand);

                const canSplit = (hand.length === 2 && getCardValue(hand[0]) === getCardValue(hand[1])) && balance >= handBets[activeHandIdx];
                const canDouble = (hand.length === 2) && balance >= handBets[activeHandIdx];

                document.getElementById('btn-split').disabled = !canSplit;
                document.getElementById('btn-double').disabled = !canDouble;

                if (pScore === 21) {
                    resolveDealerTurn();
                } else {
                    updateControls();
                }
            }

            function hitAction() {
                let hand = playerHands[activeHandIdx];
                hand.push(deck.pop());
                playSound(1, 0);
                
                document.getElementById('btn-split').disabled = true;
                document.getElementById('btn-double').disabled = true;

                let score = calculateScore(hand);
                renderTable(true);

                if (score > 21) {
                    memeVideo.style.display = 'block';
                    memeVideo.play().catch(e => console.log("Audio blocked:", e));
                    setTimeout(nextHandOrDealer, 2000);
                } else if (score === 21) {
                    setTimeout(nextHandOrDealer, 800);
                }
            }

            function doubleAction() {
                let bet = handBets[activeHandIdx];
                if (balance < bet) return;
                balance -= bet;
                handBets[activeHandIdx] += bet;
                updateBalance();

                let hand = playerHands[activeHandIdx];
                hand.push(deck.pop());
                playSound(1, 0);

                let score = calculateScore(hand);
                renderTable(true);

                if (score > 21) {
                    memeVideo.style.display = 'block';
                    memeVideo.play().catch(e => console.log("Audio blocked:", e));
                }

                setTimeout(nextHandOrDealer, score > 21 ? 2000 : 800);
            }

            function splitAction() {
                let bet = handBets[0];
                if (balance < bet) return;
                balance -= bet;
                updateBalance();

                let hand = playerHands[0];
                playerHands = [
                    [hand[0], deck.pop()],
                    [hand[1], deck.pop()]
                ];
                handBets = [bet, bet];
                activeHandIdx = 0;

                renderTable(true);
                checkInitialState();
            }

            function standAction() {
                nextHandOrDealer();
            }

            function nextHandOrDealer() {
                if (activeHandIdx < playerHands.length - 1) {
                    activeHandIdx++;
                    renderTable(true);
                    checkInitialState();
                } else {
                    resolveDealerTurn();
                }
            }

            function resolveDealerTurn() {
                gameOver = true;
                let allBust = playerHands.every(h => calculateScore(h) > 21);
                
                if (allBust) {
                    renderTable(false);
                    calculatePayouts();
                } else {
                    let drawInterval = setInterval(() => {
                        if (calculateScore(dealerHand) < 17) {
                            dealerHand.push(deck.pop()); playSound(1, 0); renderTable(false);
                        } else {
                            clearInterval(drawInterval); calculatePayouts();
                        }
                    }, 800);
                    if (calculateScore(dealerHand) >= 17) { renderTable(false); calculatePayouts(); }
                }
            }

            function calculatePayouts() {
                let dScore = calculateScore(dealerHand);
                
                playerHands.forEach((hand, idx) => {
                    let pScore = calculateScore(hand);
                    let bet = handBets[idx];
                    if (pScore <= 21) {
                        if (dScore > 21 || pScore > dScore) {
                            balance += (pScore === 21 && hand.length === 2) ? bet * 2.5 : bet * 2;
                        } else if (pScore === dScore) {
                            balance += bet;
                        }
                    }
                });

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
                document.getElementById('btn-bet').disabled = (!gameOver || waitingForInsurance);
                document.getElementById('btn-hit').disabled = (gameOver || waitingForInsurance);
                document.getElementById('btn-stand').disabled = (gameOver || waitingForInsurance);
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
