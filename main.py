from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>My Free Site</title>
        </head>
        <body>
            <h1>Welcome to my permanent free website!</h1>
            <p>I will build my Blackjack game here.</p>
        </body>
    </html>
    """