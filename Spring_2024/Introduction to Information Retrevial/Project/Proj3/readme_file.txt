The Indexer is a crucial component of an Information Retrieval (IR) Engine, which also includes a Text Parser and a Retriever. The Indexer's role is to create a forward index and an inverted index for a large document collection, which are essential for query processing and retrieval in the vector space model.

Dependencies:
- Python 3.x
- `nltk` package (for PorterStemmer)

Usage:
1. Ensure all required dependencies are installed.
2. Place the TREC document collection in the same directory as `indexer.py`.
3. Run the `indexer.py` script.
4. Forward and inverted index files will be saved as `forward_index.txt` and `inverted_index.txt`, respectively.

Forward Index File Format:
- Each document's forward index contains a list of terms.
- Format: `docID: wordID1: freq in docID; wordID2: freq in docID; ...`

Inverted Index File Format:
- For each term, the inverted index maintains a list of documents.
- Format: `wordID: docId1: freq in docId1; docId2: freq in docId2; ...`

Notes:
- The `indexer.py` includes a stopword list and the Porter stemmer algorithm.
- The code assumes the TREC document collection is in the same directory and follows the same file format as the example provided. Modify the code if your collection differs.
- Credits to the creators of the TREC document collection and the nltk package for the PorterStemmer.

