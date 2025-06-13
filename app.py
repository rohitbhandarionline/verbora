from flask import Flask, request, render_template

app = Flask(__name__)

def generate_brand_profile(info):
    return {
        "industry": info['industry'],
        "target_audience": info['target_audience'],
        "values": info['values'],
        "tone": info['tone'],
        "keywords": info['keywords'],
        "brand_story": f"A {info['tone']} brand in the {info['industry']} industry, focused on serving {info['target_audience']} with values like {', '.join(info['values'])}.",
        "positioning": f"Positioned as a {info['tone']} choice in the {info['industry']} sector, committed to {', '.join(info['values'])}."
    }

def suggest_brand_names(keywords):
    base_words = ["ly", "hub", "ify", "nest", "verse", "loop", "mint"]
    suggestions = []
    for kw in keywords:
        for base in base_words:
            suggestions.append(f"{kw.strip().capitalize()}{base}")
    return suggestions[:10]  # Return top 10

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        info = {
            'industry': request.form['industry'],
            'target_audience': request.form['audience'],
            'values': [v.strip() for v in request.form['values'].split(',')],
            'tone': request.form['tone'],
            'keywords': [k.strip() for k in request.form['keywords'].split(',')]
        }
        profile = generate_brand_profile(info)
        names = suggest_brand_names(info['keywords'])
        return render_template('result.html', profile=profile, names=names)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
