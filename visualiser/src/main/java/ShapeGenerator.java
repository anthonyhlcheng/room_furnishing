import javafx.util.Pair;

import java.awt.geom.Path2D;
import java.util.ArrayList;

public class ShapeGenerator {
    private Double COORDINATE_SCALE = 10.0;
    public Double minX = -50.0;
    public Double minY = -50.0;
    private ArrayList<Path2D> paths = new ArrayList<>();

    ShapeGenerator(){

    }
    ShapeGenerator(ArrayList<String> coordinates){
        for(String str:coordinates){
            create(str);
        }
    }

    void create(String coordinates){
        StringToCoordinates converter = new StringToCoordinates(coordinates);
        ArrayList<Pair<Double,Double>> pairs = converter.getCoordinates();
        create(pairs);
    }
    void create(ArrayList<Pair<Double,Double>> coordinates){
        Path2D path = new Path2D.Double();
        boolean isFirst = true;
        for(Pair<Double,Double> pair:coordinates){
            Double x = pair.getKey();
            Double y = pair.getValue();

            //This is only to ensure that no path will be outside of the GUI
            if(x * COORDINATE_SCALE < minX){
                minX = x * COORDINATE_SCALE;
            }
            if(y * COORDINATE_SCALE < minY){
                minY = y * COORDINATE_SCALE;
            }
            //This is required in the ROOM class for instance to ensure padding

            if(isFirst) {
                path.moveTo(x * COORDINATE_SCALE,y * COORDINATE_SCALE);
                isFirst = false;
            }else{
                path.lineTo(x * COORDINATE_SCALE,y * COORDINATE_SCALE);
            }
        }
        path.closePath();
        paths.add(path);
    }

    public Pair<Double, Double> calculateMaxWidthAndHeight(ArrayList<Pair<Double, Double>> coordinates) {
        Double maxX = 0.0;
        Double minX = Double.MAX_VALUE;
        Double minY = Double.MAX_VALUE;
        Double maxY = 0.0;
        Double diffInX = 0.0;
        Double diffInY = 0.0;
        for(Pair<Double,Double> pair:coordinates) {
            Double x = pair.getKey();
            Double y = pair.getValue();
            //get max values
            if (x > maxX) {
                maxX = x;
            }
            if (y > maxY) {
                maxY = y;
            }

            //get min values
            if (x < minX) {
                minX = x;
            }
            if (y < minY) {
                minY = y;
            }

            //get differences
            diffInX = maxX - minX;
            diffInY = maxY - minY;
        }
        return new Pair<>(diffInX, diffInY);
    }

    public void changeCoordinateScale(Double scale){
        this.COORDINATE_SCALE = scale;
    }

    public ArrayList<Path2D> getPaths() {
        return paths;
    }
}
