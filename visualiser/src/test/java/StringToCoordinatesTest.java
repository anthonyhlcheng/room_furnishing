import javafx.util.Pair;
import org.junit.Test;

import java.util.ArrayList;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.*;

public class StringToCoordinatesTest {
    StringToCoordinates converter;
    @Test
    public void areStringCostsRemovedAndCoordinatesConverted(){
        String test = "10:(0, 0), (0, 1), (0, 2)";
        converter = new StringToCoordinates(test);
        ArrayList<Pair<Double, Double>> pairs = new ArrayList<>();
        pairs.add(new Pair<>(0.0,0.0));
        pairs.add(new Pair<>(0.0,1.0));
        pairs.add(new Pair<>(0.0,2.0));
        assertThat(pairs,is(converter.getCoordinates()));
    }
    @Test
    public void areNormalCoordinatesConverted(){
        String coordinates = "(0, 0), (2, 0), (0, 0), (2, 1), (1, 1), (1, 2), (0, 2)";
        converter = new StringToCoordinates(coordinates);
        ArrayList<Pair<Double, Double>> pairs = new ArrayList<>();
        pairs.add(new Pair<>(0.0,0.0));
        pairs.add(new Pair<>(2.0,0.0));
        pairs.add(new Pair<>(0.0,0.0));
        pairs.add(new Pair<>(2.0,1.0));
        pairs.add(new Pair<>(1.0,1.0));
        pairs.add(new Pair<>(1.0,2.0));
        pairs.add(new Pair<>(0.0,2.0));
        assertThat(pairs, is(converter.getCoordinates()));
    }
}