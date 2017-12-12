import java.awt.*;
import java.util.ArrayList;
import java.util.Collections;

public class ColorIntensity {

    public ColorIntensity(ArrayList<Float> weightages) {
        ArrayList<Float> intensity = null;
        Float minimum = Collections.min(weightages);
        Float maximum = Collections.max(weightages);
        for(Float weightage : weightages) {
            intensity.add(calculateIntensity(weightage, minimum, maximum));
        }
        Graphics2D g2d = null;
        for(Float rgbvalue : intensity) {
            g2d.setPaint(new Color(rgbvalue, rgbvalue, new Float(1.0)));
        }
    }

    private Float calculateIntensity(Float weightage, Float minimum, Float maximum) {
        return weightage * (1 / (maximum - minimum + 1));
    }

}
