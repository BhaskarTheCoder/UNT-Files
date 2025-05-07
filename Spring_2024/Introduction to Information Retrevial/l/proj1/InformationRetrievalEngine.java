import java.io.*;
import java.util.*;

public class InformationRetrievalEngine {
    private static String stopwordListPath = "stopwordlist.txt";
    private static Map<String, Integer> idf = new HashMap<>();
    private static Map<String, Map<String, Integer>> vectors = new HashMap<>();
    private static Map<Integer, Integer> relevantNum = new HashMap<>();
    private static Map<Integer, Map<String, Integer>> docQueryRelevance = new HashMap<>();
    private static List<String> stopwords = new ArrayList<>();
    private static int N = 0;
    private static Porter ps = new Porter();

    public static void main(String[] args) {
        try {
            loadStopwords();
            calculateIDF();
            calculateTFIDF();
            processQueries();
            processTopics(); // Add this line to process topics
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void loadStopwords() {
        try (BufferedReader reader = new BufferedReader(new FileReader(stopwordListPath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                stopwords.add(line.trim().toLowerCase());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void calculateIDF() throws IOException {
        File folder = new File("ft911");
        File[] fileList = folder.listFiles();
        int i = 1;
        if (fileList != null) {
            for (File file : fileList) {
                try (BufferedReader br = new BufferedReader(new FileReader(file))) {
                    StringBuilder sb = new StringBuilder();
                    String line = br.readLine();
                    while (line != null) {
                        sb.append(line);
                        sb.append(System.lineSeparator());
                        line = br.readLine();
                    }
                    String text = sb.toString();
                    String[] documents = text.split("<DOC>");
                    for (String document : documents) {
                        if (document.trim().endsWith("</DOC>")) {
                            N++;
                            String docNo = extractSection(document, "<DOCNO>", "</DOCNO>").trim();
                            String docText = extractSection(document, "<TEXT>", "</TEXT>").trim();
                            String[] docTokens = tokenise(docText);
                            Map<String, Integer> vector = new HashMap<>();
                            for (String token : docTokens) {
                                vector.put(token, vector.getOrDefault(token, 0) + 1);
                            }
                            for (String token : vector.keySet()) {
                                idf.put(token, idf.getOrDefault(token, 0) + 1);
                            }
                            vectors.put(docNo, vector);
                        }
                    }
                }
            }
        }
        for (String key : idf.keySet()) {
            idf.put(key, (int) Math.log10(N / idf.get(key)));
        }
    }

    private static void calculateTFIDF() {
        for (String key : vectors.keySet()) {
            Map<String, Integer> vector = vectors.get(key);
            Map<String, Integer> tfidfVector = new HashMap<>();
            for (String token : vector.keySet()) {
                int tf = vector.get(token);
                double tfidf = (1 + Math.log10(tf)) * idf.getOrDefault(token, 0);
                tfidfVector.put(token, (int) tfidf);
            }
            vectors.put(key, tfidfVector);
        }
    }

    private static void processQueries() throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader("main.qrels"))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.trim().split("\\s+");
                int queryNumber = Integer.parseInt(parts[0]);
                String docName = parts[2];
                int relevance = Integer.parseInt(parts[3]);
                relevantNum.put(queryNumber, relevantNum.getOrDefault(queryNumber, 0) + relevance);
                docQueryRelevance.computeIfAbsent(queryNumber, k -> new HashMap<>()).put(docName, relevance);
            }
        }
        double sumPrecision = 0;
        double sumRecall = 0;
        FileWriter fw = new FileWriter("vsm_output.txt");
        for (String queryId : vectors.keySet()) {
            Map<String, Integer> queryVector = vectors.get(queryId);
            Map<String, Double> similarity = new HashMap<>();
            for (String docId : queryVector.keySet()) {
                Map<String, Integer> docVector = vectors.getOrDefault(docId, new HashMap<>());
                double cosSim = cosineSimilarity(queryVector, docVector);
                similarity.put(docId, cosSim);
            }
            List<Map.Entry<String, Double>> sortedSimilarity = new ArrayList<>(similarity.entrySet());
            sortedSimilarity.sort(Map.Entry.comparingByValue(Comparator.reverseOrder()));
            int relevantCount = 0;
            for (int rank = 0; rank < 5 && rank < sortedSimilarity.size(); rank++) {
                String docId = sortedSimilarity.get(rank).getKey();
                double score = sortedSimilarity.get(rank).getValue();
                fw.write(queryId + "    " + docId + "     " + (rank + 1) + "     " + score + "\n");
                if (docQueryRelevance.containsKey(queryId) && docQueryRelevance.get(queryId).containsKey(docId)
                        && docQueryRelevance.get(queryId).get(docId) == 1) {
                    relevantCount++;
                }
            }
            double precision = relevantCount / 5.0;
            double recall = (double) relevantCount / relevantNum.getOrDefault(queryId, 1);
            sumPrecision += precision;
            sumRecall += recall;
        }
        double meanPrecision = sumPrecision / vectors.size();
        double meanRecall = sumRecall / vectors.size();
        System.out.println("Mean Precision: " + meanPrecision);
        System.out.println("Mean Recall: " + meanRecall);
        fw.close();
    }

    private static String[] tokenise(String document) {
        document = document.toLowerCase().replaceAll("[^a-zA-Z0-9\\s]", "");
        return document.split("\\s+");
    }

    private static String extractSection(String text, String start, String end) {
        int startIndex = text.indexOf(start) + start.length();
        int endIndex = text.indexOf(end);
        return text.substring(startIndex, endIndex).trim();
    }

    private static double cosineSimilarity(Map<String, Integer> vector1, Map<String, Integer> vector2) {
        double dotProduct = 0;
        double vector1Mag = 0;
        double vector2Mag = 0;
        for (String key : vector1.keySet()) {
            dotProduct += vector1.get(key) * vector2.getOrDefault(key, 0);
            vector1Mag += Math.pow(vector1.get(key), 2);
        }
        for (String key : vector2.keySet()) {
            vector2Mag += Math.pow(vector2.get(key), 2);
        }
        vector1Mag = Math.sqrt(vector1Mag);
        vector2Mag = Math.sqrt(vector2Mag);
        return dotProduct / (vector1Mag * vector2Mag);
    }

    private static Map<Integer, Map<String, Integer>> titleVector = new HashMap<>();
    private static Map<Integer, Map<String, Integer>> titleDescVector = new HashMap<>();
    private static Map<Integer, Map<String, Integer>> titleNarrVector = new HashMap<>();

    private static Map<String, Integer> calculateTFIDF2(String key, String[] tokens) {
        Map<String, Integer> vector = new HashMap<>();
        for (String token : tokens) {
            vector.put(token, vector.getOrDefault(token, 0) + 1);
        }

        Map<String, Integer> tfidfVector = new HashMap<>();
        for (String token : vector.keySet()) {
            int tf = vector.get(token);
            double tfidf = (1 + Math.log10(tf)) * idf.getOrDefault(token, 0);
            tfidfVector.put(token, (int) tfidf);
        }

        vectors.put(key, tfidfVector);
        return vector;
    }


    private static void processTopics() throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader("topics.txt"))) {
            String line;
            StringBuilder sb = new StringBuilder();
            while ((line = br.readLine()) != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
            }
            String content = sb.toString();
            String[] topics = content.split("<top>");
            for (String topic : topics) {
                if (topic.trim().endsWith("</top>")) {
                    int number = Integer.parseInt(extractSection(topic, "<num>", "<title>").trim().replaceAll("\\D", ""));
                    String title = extractSection(topic, "<title>", "<desc>").trim();
                    String description = extractSection(topic, "<desc>", "<narr>").trim();
                    String narrative = extractSection(topic, "<narr>", "</top>").trim();

                    String[] titleTokens = tokenise(title);
                    String[] titleDescTokens = tokenise(title + " " + description);
                    String[] titleNarrTokens = tokenise(title + " " + narrative);
                    titleVector.put(number,calculateTFIDF2("title_1", titleTokens));
                    titleDescVector.put(number, calculateTFIDF2("title_desc_1", titleDescTokens));
                    titleNarrVector.put(number, calculateTFIDF2("title_narr_1", titleNarrTokens));
                }
            }
        }
    }
}
