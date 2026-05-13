// https://java.godbolt.org/z/dshcTfoqE
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Collections;

class Main {
    // L, R, S
    final static Map<Integer, List<Integer>> valid_moves = Map.ofEntries(
        Map.entry(1, List.of(1, 2, 3)),
        Map.entry(2, List.of(1, 2, 6)),
        Map.entry(3, List.of(3, 4, 3)),
        Map.entry(4, List.of(3, 4, 8)),
        Map.entry(5, List.of(5, 6, 7)),
        Map.entry(6, List.of(5, 6, 6)),
        Map.entry(7, List.of(7, 8, 7)),
        Map.entry(8, List.of(7, 8, 8))
    );

    private static class Goals {
        Integer left;
        Integer right;

        public Goals(Integer l, Integer r) {
            left = l;
            right = r;
        }

        public boolean match(Integer i) {
            return i == left || i == right;
        }
    };

    public static void main(String args[]) {
        final List<Integer> problemset = new ArrayList<>(List.of(1, 2, 3, 4, 5, 6, 7, 8));
        ArrayList<Boolean> visited = new ArrayList<>(Collections.nCopies(8, false));
        final Goals goal = new Goals(7, 8);

        ArrayDeque<Integer> beingVisited = new ArrayDeque<Integer>();
        beingVisited.add(problemset.get(0));

        while (beingVisited.size() != 0) {
            final Integer current = beingVisited.remove();
            System.out.println("visiting: " + current);
            visited.set(current - 1, true);

            if (goal.match(current)) {
                System.out.println("Found goal");
                break;
            }

            for (final Integer elem: valid_moves.get(current)) {
                if (!visited.get(elem - 1)) { 
                    beingVisited.add(elem);
            }
            }
        }
    }
}
