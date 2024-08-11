import spacy
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords (if not already downloaded)
nltk.download('stopwords')

nlp = spacy.load("en_core_web_sm")  # Load the spaCy English model

def preprocess_text(text):
    """
    Preprocesses the given text by tokenizing, cleaning, and lemmatizing.

    Args:
        text (str): The text to preprocess.

    Returns:
        list: A list of preprocessed tokens (lemmatized words).
    """

    doc = nlp(text)

    # Tokenization and cleaning
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]

    # Lemmatization
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

    return lemmatized_tokens

def extract_entities(text):
    """
    Extracts named entities from the given text using spaCy's NER.

    Args:
        text (str): The text to process.

    Returns:
        list: A list of tuples containing entity text and label (e.g., [("Apple Inc.", "ORG"), ("Tim Cook", "PERSON")]).
    """

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def extract_relationships(text):
    """
    Extracts relationships between entities in the given text using dependency parsing.

    Args:
        text (str): The text to process.

    Returns:
        list: A list of tuples representing relationships (e.g., [("Apple Inc.", "headquartered in", "Cupertino")]).
    """

    doc = nlp(text)
    relationships = []

    for token in doc:
        if token.dep_ in ["nsubj", "dobj", "prep", "pobj"]:  # Consider key dependency types
            subject = [child for child in token.head.children if child.dep_ == "nsubj"]
            subject = subject[0] if subject else token.head  # Handle cases where subject is implicit
            relationships.append((subject.text, token.text, token.head.text))

    return relationships
def split_into_sentences(text):
    """
    Splits a text into sentences using spaCy's sentence segmentation.

    Args:
        text (str): The text to split.

    Returns:
        list: A list of sentences.
    """
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

def process_text_in_chunks(text, chunk_size=20):
    """
    Processes a large text in chunks to manage memory usage.

    Args:
        text (str): The text to process.
        chunk_size (int): The number of sentences per chunk.

    Returns:
        list: A list of extracted entities from all chunks.
        list: A list of extracted relationships from all chunks
    """

    sentences = split_into_sentences(text)
    all_entities = []
    all_relationships = []

    # Parallel processing (optional, requires spacy >= 3.0)
    if spacy.__version__.startswith('3'):
        for doc in nlp.pipe(sentences, batch_size=chunk_size, n_process=-1):  # Use all available cores
            chunk_entities = extract_entities(doc.text)
            chunk_relationships = extract_relationships(doc.text)
            all_entities.extend(chunk_entities)
            all_relationships.extend(chunk_relationships)
    else: 
        # Sequential processing (for older spaCy versions or if parallel processing is not desired)
        for i in range(0, len(sentences), chunk_size):
            chunk = sentences[i:i + chunk_size]
            chunk_text = " ".join(chunk)

            chunk_entities = extract_entities(chunk_text)
            chunk_relationships = extract_relationships(chunk_text)

            all_entities.extend(chunk_entities)
            all_relationships.extend(chunk_relationships)

    return all_entities, all_relationships