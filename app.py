from flask import Flask, request, render_template, redirect, flash
import csv
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

# Generate a brand profile from user input
def generate_brand_profile(info):
    return {
        "industry": info['industry'],
        "target_audience": info['target_audience'],
        "values": info['values'],
        "tone": info['tone'],
        "keywords": info['keywords'],
        "brand_story": (
            f"A {info['tone']} brand in the {info['industry']} industry, "
            f"focused on serving {info['target_audience']} with values like {', '.join(info['values'])}."
        ),
        "positioning": (
            f"Positioned as a {info['tone']} choice in the {info['industry']} sector, "
            f"committed to {', '.join(info['values'])}."
        )
    }

# Suggest brand names based on keywords
def suggest_brand_names(keywords):
    base_words = ["ly", "hub", "ify", "nest", "verse", "loop", "mint"]
    suggestions = [
        f"{kw.strip().capitalize()}{base}" 
        for kw in keywords 
        for base in base_words
    ]
    return suggestions[:10]

# Save email and associated profile
@app.route('/save_email', methods=['POST'])
def save_email():
    email = request.form.get('email')
    profile_json = request.form.get('profile_json')

    if email and profile_json:
        try:
            with open('emails.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([email, profile_json])
            flash("✅ Your profile has been saved and emailed!", "success")
        except Exception as e:
            flash(f"❌ Error saving email: {str(e)}", "error")
    else:
        flash("❌ Missing email or profile data.", "error")

    return redirect('/')

# Main page to submit brand details
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
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='127.0.0.1', port=5000, debug=True)
