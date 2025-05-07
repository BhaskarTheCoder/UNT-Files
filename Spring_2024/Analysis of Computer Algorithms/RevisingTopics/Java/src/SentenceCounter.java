import java.util.*;
// Time is in seconds since arrived in the event.
// Entry has identification check with 5min
// If they find more than 10 people in the queue they leave.
// return an array of intergers when each people will be processed and their ID check is completed.
// If a person leaves immediately upon arrival, this time should be the same as their arrival time.
// The queue size is calculated by the number of people waiting to start their ID check, not including the person who is already in the process of ID check.

import java.util.*;

import java.util.*;
import java.util.*;

class Main {
    public static String longestCommonSuffixPath(String[] paths) {
        if (paths == null || paths.length == 0) {
            return "";
        }

        // Split each path into directory components
        List<List<String>> components = new ArrayList<>();
        for (String path : paths) {
            List<String> pathComponents = Arrays.asList(path.split("/"));
            components.add(pathComponents);
        }

        // Find the shortest path length among all paths
        int minPathLength = Integer.MAX_VALUE;
        for (List<String> pathComponents : components) {
            minPathLength = Math.min(minPathLength, pathComponents.size());
        }

        // Traverse each path from the end and find the common suffix
        StringBuilder commonSuffix = new StringBuilder();
        for (int i = 0; i < minPathLength; i++) {
            String currentComponent = components.get(0).get(components.get(0).size() - 1 - i);

            // Check if current component is valid (not "..." or special characters)
            if (!currentComponent.equals("..") && !currentComponent.isEmpty()) {
                boolean isCommon = true;
                for (int j = 1; j < components.size(); j++) {
                    String componentToCompare = components.get(j).get(components.get(j).size() - 1 - i);
                    if (!componentToCompare.equals(currentComponent)) {
                        isCommon = false;
                        break;
                    }
                }
                if (isCommon) {
                    commonSuffix.insert(0, "/" + currentComponent);
                } else {
                    break;
                }
            } else {
                break; // Stop if encountering special characters
            }
        }

        return commonSuffix.toString();
    }

    public static void main(String[] args) {
        String[] paths = {
                "/a/folder1/../folder1/a/leaf.txt",
                "/b/folder2/folder1/a/leaf.txt",
                "/a/folder3/folder1/folder1/a/leaf.txt"
        };
        String commonSuffix = longestCommonSuffixPath(paths);
        System.out.println("Longest common suffix path: " + commonSuffix); // Output: "/folder1/a/leaf.txt"
    }
}
