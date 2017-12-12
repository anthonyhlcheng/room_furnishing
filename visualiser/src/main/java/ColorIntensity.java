import java.awt.*;
import java.util.ArrayList;
import java.util.Collections;

public class ColorIntensity {
    private static final float RGB_Blue_Value = 1.0f;

    public ColorIntensity() {
        //read shapes that are not in the room from file
        String filename = "src/main/java/1.txt";
        ReadFile reader = new ReadFile(filename);
        ArrayList<String> shapesNotInRoom  = reader.getShapesNotInRoom();

        //parses the total costs and stores them in an arraylist
        ArrayList<Float> weightages = null;
        for(String shape : shapesNotInRoom) {
            String[] splitted = shape.split(":");
            weightages.add(Float.parseFloat(splitted[0]));
        }

        //calculates and returns an arraylist of rgb intensity values
        ArrayList<Float> rgbValues = calculateIntensity(weightages);

        Graphics2D g2d = null;
        for(Float rgbValue : rgbValues) {
            g2d.setPaint(new Color(rgbValue, rgbValue, RGB_Blue_Value));
        }
    }

    private ArrayList<Float> calculateIntensity(ArrayList<Float> weightages) {
        ArrayList<Float> intensities = null;
        Float minimum = Collections.min(weightages);
        Float maximum = Collections.max(weightages);
        for(Float weightage : weightages) {
            intensities.add(weightage * (1 / (maximum - minimum + 1)));
        }
        return  intensities;
    }

}
