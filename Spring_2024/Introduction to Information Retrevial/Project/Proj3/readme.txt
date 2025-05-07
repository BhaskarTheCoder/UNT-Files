The terms 'topic' and 'query' are used interchangeably.

Description and Format of 'qrels' File:
The 'main.qrels' file contains manually judged relevance judgments for each topic in the 'topics.txt' file. It is used to evaluate the performance of the system. The format is:

TOPIC    ITERATION    DOCUMENT    RELEVANCY

where
- TOPIC is the topic number,
- ITERATION is the feedback iteration (usually zero),
- DOCUMENT is the document name corresponding to the "docno" field in the documents, and
- RELEVANCY is a binary code (0 for not relevant, 1 for relevant).

Description and Format of the 'topics' File:
The 'topics' file contains queries. Each query is enclosed within <top> and </top> tags. The format of each topic is:

<num> Unique Query Number
<title> Main Query (Max. three words)
<desc> One-sentence description of the query
<narr> Concise description of what makes a document relevant

For the retrieval model, the Main Query in the <title> tag can be used. The <desc> and <narr> can be used for query expansion or to improve system precision.

Description and Format of the Query Processor Output:
The Query Processor should process all topics in batch mode and output a file with the format:

TOPIC    DOCUMENT    UNIQUE#    COSINE_VALUE

where
- TOPIC is the topic number,
- DOCUMENT is the document name corresponding to the "docno" field in the documents,
- UNIQUE# is a unique counter of the number of documents retrieved for each topic, and
- COSINE_VALUE is the cosine similarity score for each document with respect to the topic (using TF*IDF as a weighting scheme).

Each field above is separated by a TAB. Refer to 'sample_output.txt' for an example of how the Query Processor output should look.