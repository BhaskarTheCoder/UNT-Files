import java.util.*;
import java.io.*;
import java.util.stream.Collectors;
class TextParser {

    public static void main(String[] args) {
        String stopwordListPath = "stopwordlist.txt";
        // Parse documents and store text content
        Map<String, String> docNoToTextContent = parseDocuments();
        // Load stopword list
        StopwordRemover stopwordRemover = loadStopwords(stopwordListPath);
        // Tokenize text content, remove stopwords, and create WordDictionary
        Map<String, Integer> wordDictionary = createWordDictionary(docNoToTextContent, stopwordRemover);
        // Create FileDictionary
        Map<String, Integer> fileDictionary = createFileDictionary(docNoToTextContent);
        // Output WordDictionary and FileDictionary to parser_output.txt
        writeOutput("parser_output.txt", wordDictionary, fileDictionary);

        Indexer indexer = new Indexer();
        Porter stemmer = new Porter();
        indexer.buildIndices(docNoToTextContent, wordDictionary, stopwordRemover, stemmer);

        try {
            indexer.writeInvertedIndex("inverted_index.txt");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    private static Map<String, String> parseDocuments() {
        Map<String, String> docNoToTextContent = new LinkedHashMap<>();
        File folder = new File("ft911");
        File[] fileList = folder.listFiles();
        int i = 1;
        if (fileList != null) {
            for (File file : fileList) {
                String path = "ft911/ft911_" + (i++) + ".txt";
                try (BufferedReader br = new BufferedReader(new FileReader(path))) {

                    String docNo = null;
                    StringBuilder contentBuilder = new StringBuilder();
                    boolean isTextTag = false;
                    String line;

                    while ((line = br.readLine()) != null) {
                        if (line.contains("<DOCNO>")) {
                            docNo = line.substring(line.indexOf("<DOCNO>") + 7, line.indexOf("</DOCNO>")).trim();
                        } else if (line.contains("<TEXT>")) {
                            isTextTag = true;
                            contentBuilder.setLength(0);
                        } else if (line.contains("</TEXT>")) {
                            isTextTag = false;
                            docNoToTextContent.put(docNo, contentBuilder.toString());
                        } else if (isTextTag) {
                            contentBuilder.append(line).append("\n");
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return docNoToTextContent;
    }

    private static Map<String, Integer> createWordDictionary(Map<String, String> docNoToTextContent, StopwordRemover stopwordRemover) {
        Map<String, Integer> wordDictionary = new LinkedHashMap<>();
        int tokenId = 1;
        Porter stemmer = new Porter();
        for (String textContent : docNoToTextContent.values()) {
            String[] tokens = textContent.split("\\s+"); // Split on whitespace
            for (String token : tokens) {
                token = token.toLowerCase().replaceAll("[^a-z]", ""); // Remove non-letter characters and convert to lower case
                if (!token.matches(".*\\d.*") && !token.isEmpty() && !stopwordRemover.isStopword(token)) { // Ignore tokens with numbers and stopwords
                    String stemmedToken = stemmer.stripAffixes(token);
                    if (!wordDictionary.containsKey(stemmedToken)) {
                        wordDictionary.put(stemmedToken, tokenId++);
                    }
                }
            }
        }
        return wordDictionary;
    }


    // Function to create FileDictionary
    private static Map<String, Integer> createFileDictionary(Map<String, String> docNoToTextContent) {
        Map<String, Integer> fileDictionary = new LinkedHashMap<>();
        int docId = 1;
        for (String docNo : docNoToTextContent.keySet()) {
            fileDictionary.put(docNo, docId++);
        }
        return fileDictionary;
    }

    // Function to write WordDictionary and FileDictionary to file
    private static void writeOutput(String filename, Map<String, Integer> wordDictionary, Map<String, Integer> fileDictionary) {
        try (PrintWriter writer = new PrintWriter(filename)) {
            for (Map.Entry<String, Integer> entry : wordDictionary.entrySet()) {
                writer.println(entry.getKey() + "\t\t" + entry.getValue());
            }
            writer.println("..........");
            for (Map.Entry<String, Integer> entry : fileDictionary.entrySet()) {
                writer.println(entry.getKey() + "\t\t" + entry.getValue());
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    // Function to load stopword list
    private static StopwordRemover loadStopwords(String filename) {
        StopwordRemover stopwordRemover = new StopwordRemover(filename);
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                stopwordRemover.addStopword(line.trim().toLowerCase());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return stopwordRemover;
    }
}

class StopwordRemover {
    private Set<String> stopwords;

    public StopwordRemover(String stopwordFile) {
        stopwords = new HashSet<>();
        loadStopwords(stopwordFile);
    }

    private void loadStopwords(String stopwordFile) {
        try (BufferedReader reader = new BufferedReader(new FileReader(stopwordFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                stopwords.add(line.trim().toLowerCase());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean isStopword(String word) {
        return stopwords.contains(word.toLowerCase());
    }

    public void addStopword(String word) {
        stopwords.add(word.toLowerCase());
    }
}

class Indexer {
    // Inverted Index: Word ID -> Map of (Document ID -> Frequency)
    private Map<Integer, Map<Integer, Integer>> invertedIndex = new HashMap<>();

    // This will build the inverted index given the document contents and the word dictionary
    public void buildIndices(Map<String, String> docNoToTextContent, Map<String, Integer> wordDictionary, StopwordRemover stopwordRemover, Porter stemmer) {
        // For each document...
        for (Map.Entry<String, String> docEntry : docNoToTextContent.entrySet()) {
            String docID = docEntry.getKey();
            String content = docEntry.getValue();

            // Convert document ID to numeric form, stripping out non-digit characters
            int numericDocID;
            try {
                numericDocID = Integer.parseInt(docID.replaceAll("[^\\d]", ""));
            } catch (NumberFormatException e) {
                System.err.println("Invalid document ID format: " + docID);
                continue; // Skip this document and continue with the next
            }

            // Tokenize and stem each word in the document
            StringTokenizer tokenizer = new StringTokenizer(content, " \t\n\r\f.,;:\"'?!-()[]{}");
            while (tokenizer.hasMoreTokens()) {
                String token = tokenizer.nextToken().toLowerCase();
                // Check if the token is a number or contains a number
                if (!token.matches(".*\\d+.*")) {
                    // Apply the Porter stemmer
                    String stemmedToken = stemmer.stripAffixes(token);
                    if (!stemmedToken.isEmpty() && !stopwordRemover.isStopword(stemmedToken)) {
                        // Get the word ID from the word dictionary
                        Integer wordId = wordDictionary.get(stemmedToken);
                        if (wordId != null) {
                            // Update the inverted index
                            invertedIndex.computeIfAbsent(wordId, k -> new HashMap<>())
                                    .merge(numericDocID, 1, Integer::sum);
                        }
                    }
                }
            }
        }
    }
    // Method to write the inverted index to a file
    public void writeInvertedIndex(String filename) throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            for (Map.Entry<Integer, Map<Integer, Integer>> entry : invertedIndex.entrySet()) {
                Integer wordId = entry.getKey();
                Map<Integer, Integer> docFreqs = entry.getValue();
                // Start the line with the wordID
                writer.print(wordId + ": ");
                // For each document in which the word appears...
                for (Map.Entry<Integer, Integer> docEntry : docFreqs.entrySet()) {
                    Integer docId = docEntry.getKey();
                    Integer freq = docEntry.getValue();
                    // Write the document and frequency information
                    writer.print(docId + ": " + freq + "; ");
                }
                // End the line after each word's document list
                writer.println();
            }
        }
    }


    // Getters for testing or further processing
    public Map<Integer, Map<Integer, Integer>> getInvertedIndex() {
        return invertedIndex;
    }
}

