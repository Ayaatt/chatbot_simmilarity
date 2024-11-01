from flask import Flask, request, render_template_string, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import time
import requests
import math


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///similarity.db'
db = SQLAlchemy(app)

original_query = "trun no the lamb"
devices = ["tv", "fan", "pc", "lamp", "television"]
states_on = ["turn on", "off", "activation", "active"]
states_off = ["turn off", "off", "terminate", "deactive"]


def tokenize(query):
    return query.lower().split()

def jakar(str1, str2):
    set1 = set(str1)
    set2 = set(str2)

    # Menghitung irisan dan gabungan karakter
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    # Menghitung skor Jaccard
    if not union:
        return 0
    return len(intersection) / len(union)

def jaccard_similarity(user, dicti, similarity_threshold=0.2):
    tokens = user.lower().split()
    kalimat_benar = []
    for kata in tokens:
        # kata_set = set(kata)
        # kondisi = False
        if kata in [".", ",", "!", "?", ":", ";", "the"]:
            kalimat_benar.append(kata)
            continue
        best_match = max(
            dicti, key=lambda dict_word: jakar(kata, dict_word))
        kalimat_benar.append(best_match)

    # Menggabungkan token yang telah dikoreksi
    return ' '.join(kalimat_benar)

def commands(order):
    results = tokenize(order)
    
    for token in results:
        if token in states_off:
            print(states_off)
        elif token in states_on:
            print(state_on)
        print(token)


@app.route('/corrected_string', methods=['POST', 'GET'])
def similarity():
    if request.method == 'POST':
        time_start = time.time()
        body = request.get_json()
        user_query = body['input']
        tokens = user_query.lower().split()
        corrected_sentence = []

        for token in tokens:
            if token in [".", ",", "!", "?", ":", ";", "the"]:
                corrected_sentence.append(token)
                continue

        # Find the closest match
            closest_match = None
            max_shared_letters = 0
            
            dictionary = (devices + states_on + states_off)
            

            for word in dictionary:
                # Count shared letters
                shared_letters = len(set(token) & set(word))
                if shared_letters > max_shared_letters:
                    max_shared_letters = shared_letters
                    closest_match = word

            print(f"Shared Letters: {shared_letters}")
            print(f"Max Shared Letters: {max_shared_letters}")
            print(f"Closest Match: {closest_match}")

            # Append the closest match or the original word if no match was found
            if closest_match and max_shared_letters > 0:
                corrected_sentence.append(closest_match)
            else:
                corrected_sentence.append(token)
                
        result_sentences = ' '.join(corrected_sentence)
        commands(result_sentences)
        
        print(f"Original Query: {user_query}")
        print(f"Corrected Sentence: {' '.join(corrected_sentence)}")
        time_end = time.time()
        total_time = time_end - time_start
        print(f"Execution Time: {time_end - time_start}")
        
        return jsonify({"output": result_sentences, "time": total_time}), 200
    else:
        return jsonify({"message": "Please send a POST request"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
