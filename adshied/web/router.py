from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    top_blocked_domains=[
            ("ads.com", random.randint(1, 100)),
            ("analytics.org", random.randint(1, 100)),
            ("getstatus.example.it", random.randint(1, 100)),
            ("cdn.ads.com", random.randint(1, 100)),
        ]
    top_blocked_domains.sort(key=lambda x: x[1], reverse=True)

    return render_template(
        'index.html',
        blocked_ads=random.randint(0, 100),
        total_requests=random.randint(1000, 50000),
        unique_domains=random.randint(1, 100),
        top_blocked_domains=top_blocked_domains,
        )
