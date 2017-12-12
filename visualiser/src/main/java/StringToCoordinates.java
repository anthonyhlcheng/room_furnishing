import javafx.util.Pair;

import java.util.ArrayList;

/*
This class can convert a string in the format of (0, 0), (0, 1) .... OR 10:(0, 0), (0, 1) .... into Coordinate Pairs
 */
public class StringToCoordinates {

    private ArrayList<Pair<Double, Double>> coordinates = new ArrayList<>();

    private String costRemoval(String str){
        //If this method is activated then the string must be of format [10: (0, 0), ...] We need to remove the cost
        int index = str.indexOf(":");
        return str.substring(index+1);
    }
    StringToCoordinates(String str){
        if(str.indexOf(":") > 0){
            str = costRemoval(str);
        }
        str = str.replace(" ","").replace("),(", ")/(");
        String[] coordinateArray = str.split("/");
        for(String coordinate:coordinateArray){
            //System.out.println(coordinate);
            int commaLocation = coordinate.indexOf(",");
            Double x = Double.parseDouble(coordinate.substring(1,commaLocation));
            Double y = Double.parseDouble(coordinate.substring(commaLocation+1, coordinate.length()-1));
            coordinates.add(new Pair<>(x,y));
        }
    }

    public ArrayList<Pair<Double, Double>> getCoordinates() {
        return coordinates;
    }
}
