from flask import Flask, render_template, request
import requests

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

GAME_ALIASES = {
    "fifa26": "EA SPORTS FC",
    "fc26": "EA SPORTS FC",
    "gta5": "Grand Theft Auto V",
    "cs2": "Counter-Strike 2"
}

REGIONS = {
    "TR": {"name": "Türkiye 🇹🇷", "cc": "tr"},
    "US": {"name": "Amerika 🇺🇸", "cc": "us"},
    "DE": {"name": "Almanya 🇩🇪", "cc": "de"},
    "GB": {"name": "İngiltere 🇬🇧", "cc": "gb"}
}

@app.route('/', methods=["GET", "POST"])
def home():
    selected_region = "TR"
    searched_game = ""
    main_game = None
    extras = []
    not_found = False

    if request.method == "POST":
        selected_region = request.form.get("region", "TR")
        searched_game = request.form.get("game_name", "").strip()

        if searched_game:
            cleaned_input = searched_game.lower().replace(" ", "")
            search_term = GAME_ALIASES.get(cleaned_input, searched_game)

            region_cc = REGIONS.get(selected_region, REGIONS["TR"])["cc"]
            search_url = f"https://store.steampowered.com/api/storesearch/?term={search_term}&l=turkish&cc={region_cc}"

            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                items = response.json().get("items", [])
                if items:
                    main_game = items[0]
                    extras = items[1:5]
                else:
                    not_found = True

    return render_template(
        "index.html",
        selected_region=selected_region,
        region_name=REGIONS.get(selected_region, REGIONS["TR"])["name"],
        searched_game=searched_game,
        main_game=main_game,
        extras=extras,
        not_found=not_found
    )

if __name__ == "__main__":
    app.run(debug=True)
