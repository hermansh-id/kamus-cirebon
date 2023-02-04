from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv, time
import Levenshtein
import uvicorn
import regex as re
app = FastAPI()

class Item(BaseModel):
    sentence: str
    mode: str

class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, meaning):
        node = self.root
        for i in word:
            if i not in node.children:
                node.children[i] = TrieNode()
            node = node.children[i]
        node.end_of_word = meaning
    
    def search(self, word):
        node = self.root
        for i in word:
            if i not in node.children:
                return None
            node = node.children[i]
        if node.end_of_word:
            return node.end_of_word
        else:
            return None

def create_trie(data):
    trie = Trie()
    for row in data:
        trie.insert(row[2], (row[0], row[1]))
    return trie

def translate(sentence, mode):
    with open('data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = [row for row in reader]
    
    translations = {}
    for row in rows:
        translations[row[2]] = [row[0], row[1]]
    
    words = sentence.split()
    words = [i.lower() for i in words]
    trie = create_trie(rows)
    translated_sentence = []
    for word in words:
        word = re.sub(r'([^\d\w\s])', '', word)
        if(len(re.findall(r"(\d)", word)) > 0):
            translated_sentence.append(word)
            continue
        search_result = trie.search(word)
        if search_result:
            if mode == "cerbon":
                translated_sentence.append(translations[word][0])
            elif mode == "bebasan":
                translated_sentence.append(translations[word][1])
        else:
            closest_word = None
            closest_distance = float('inf')
            for key in translations:
                distance = Levenshtein.distance(word, key)
                if distance < closest_distance:
                    closest_word = key
                    closest_distance = distance
            if mode == "cerbon":
                translated_sentence.append("!"+translations[closest_word][0])
            elif mode == "bebasan":
                translated_sentence.append("!"+translations[closest_word][1])
    return " ".join(translated_sentence)

@app.post("/translate/")
def translate_sentence(item: Item):
    try:
        start_time = time.time()
        translation = translate(item.sentence, item.mode)
        end_time = time.time()
        total_time = end_time - start_time
        return {"translation": translation, "time_taken": total_time}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: Invalid Input")
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)