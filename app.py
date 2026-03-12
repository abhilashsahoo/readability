from flask import Flask, request, jsonify
import textstat
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import math

app = Flask(__name__)
CORS(app)  # Initialize CORS with your app

def fetch_content_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return ' '.join([p.get_text() for p in soup.find_all('p')])
    except requests.RequestException as e:
        return None
        
def custom_round(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
    
def normalize_score(score, original_range):
    min_original, max_original = original_range
    min_new, max_new = (0, 100)

    normalized = (score - min_original) / (max_original - min_original) * (max_new - min_new) + min_new
    return normalized

@app.route('/readability', methods=['POST'])
def readability():
    data = request.get_json()
    
    if 'text' in data:
        content = data['text']
    elif 'url' in data:
        content = fetch_content_from_url(data['url'])
        if not content:
            return jsonify({'error': 'Failed to fetch content from the provided URL'}), 400
    else:
        return jsonify({'error': 'No text or URL provided'}), 400

    score_ranges = {
        'flesch_reading_ease': (0, 100),
        'smog_index': (0, 25),
        'flesch_kincaid_grade': (0, 25),
        'coleman_liau_index': (0, 25),
        'automated_readability_index': (0, 25),
        'dale_chall_readability_score': (0, 10),
        'linsear_write_formula': (0, 25),
        'gunning_fog': (0, 25)
    }

    normalized_scores = []
    normalized_scores.append(normalize_score(textstat.flesch_reading_ease(content), score_ranges['flesch_reading_ease']))
    normalized_scores.append(normalize_score(textstat.smog_index(content), score_ranges['smog_index']))
    normalized_scores.append(normalize_score(textstat.flesch_kincaid_grade(content), score_ranges['flesch_kincaid_grade']))
    normalized_scores.append(normalize_score(textstat.coleman_liau_index(content), score_ranges['coleman_liau_index']))
    normalized_scores.append(normalize_score(textstat.automated_readability_index(content), score_ranges['automated_readability_index']))
    normalized_scores.append(normalize_score(textstat.dale_chall_readability_score(content), score_ranges['dale_chall_readability_score']))
    normalized_scores.append(normalize_score(textstat.linsear_write_formula(content), score_ranges['linsear_write_formula']))
    normalized_scores.append(normalize_score(textstat.gunning_fog(content), score_ranges['gunning_fog']))

    average_normalized_score = custom_round(sum(normalized_scores) / len(normalized_scores), 1)

    scores = {
        'flesch_reading_ease': textstat.flesch_reading_ease(content),
        'smog_index': textstat.smog_index(content),
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(content),
        'coleman_liau_index': textstat.coleman_liau_index(content),
        'automated_readability_index': textstat.automated_readability_index(content),
        'dale_chall_readability_score': textstat.dale_chall_readability_score(content),
        'difficult_words': textstat.difficult_words(content),
        'linsear_write_formula': textstat.linsear_write_formula(content),
        'gunning_fog': textstat.gunning_fog(content),
        'text_standard': textstat.text_standard(content, float_output=False),
        'average_normalized_readability': average_normalized_score,
         'reading_time': textstat.reading_time(content),
        'sentence_count': textstat.sentence_count(content),
        'character_count': textstat.char_count(content, ignore_spaces=True),
        'letter_count': textstat.letter_count(content)
    }

    return jsonify(scores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
