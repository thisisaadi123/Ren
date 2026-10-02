def validate(text, words):
    assert type(text) is str and 1 <= len(text) <= 20 and all("a" <= c <= "z" for c in text), "1 <= text.length <= 20"
    assert isinstance(words, list) and 1 <= len(words) <= 20, "1 <= words.length <= 20"
    assert all(type(w) is str and 1 <= len(w) <= 10 and all("a" <= c <= "z" for c in w) for w in words), "1 <= words[i].length <= 10"
    assert len(set(words)) == len(words), "words are all different"
