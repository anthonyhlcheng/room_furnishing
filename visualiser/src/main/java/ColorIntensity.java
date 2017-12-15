import javafx.util.Pair;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.geom.Path2D;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collections;

public class ColorIntensity extends JPanel {

    private ArrayList<Float> rgbValues = new ArrayList<>();
    private ArrayList<Pair<Path2D, Float>> drawThisPairs = new ArrayList<>();
    private ArrayList<Path2D> furnitures = new ArrayList<>();
    private static final float RGB_Blue_Value = 1.0f;
    private String room = "";
    private ArrayList<String> shapesNotInRoom  = new ArrayList<>();
    private static final Double SCALE = 2.0;
    private ArrayList<Pair<Double,Double>> shapeCoordinates = new ArrayList<>();
    private ArrayList<Pair<Double, Double>> maxCoordinates = new ArrayList<>();

    public ColorIntensity(ArrayList<String> shapesNotInRoom) {
        String filename = "C:\\Users\\zheng\\Desktop\\room_furnishing\\visualiser\\src\\main\\java\\1.txt";
        ReadFile reader = new ReadFile(filename);
        this.room = reader.getRoom();
        this.shapesNotInRoom = shapesNotInRoom;
        extractWeightage();
        getMaxWidthAndHeight();
    }

    private void getMaxWidthAndHeight() {
        for (String shape : shapesNotInRoom) {
            StringToCoordinates converter = new StringToCoordinates(shape);
            shapeCoordinates = converter.getCoordinates();
            ShapeGenerator generator = new ShapeGenerator();
            maxCoordinates.add(generator.calculateMaxWidthAndHeight(shapeCoordinates));
        }
    }

    private void extractWeightage() {
        ArrayList<Float> weightages = new ArrayList<>();
        for(String shape : shapesNotInRoom) {
            String[] splitted = shape.split(":");
            weightages.add(Float.parseFloat(splitted[0]));
        }
        calculateIntensity(weightages);
    }

    private void mapIntoPairs(ArrayList<Float> rgbValues, ArrayList<Path2D> furnitures) {
        int max = rgbValues.size() > furnitures.size() ? rgbValues.size() : furnitures.size();
        for (int i = 0; i < max; i++) {
            drawThisPairs.add(new Pair(furnitures.get(i), rgbValues.get(i)));
        }
    }

    private void drawFurnitureOutside(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        AffineTransform saveTransform = g2d.getTransform();
        ShapeGenerator generator = new ShapeGenerator(shapesNotInRoom);
        this.furnitures = generator.getPaths();
        mapIntoPairs(rgbValues, furnitures);

        try {
            //get the max width and height of the room for transformation purposes
            StringToCoordinates converter = new StringToCoordinates(room);
            ArrayList<Pair<Double, Double>> roomCoordinates = converter.getCoordinates();
            ShapeGenerator roomMax = new ShapeGenerator();
            Pair<Double, Double> roomMaxWidthAndHeight = roomMax.calculateMaxWidthAndHeight(roomCoordinates);
            //translate away from room to start drawing of shapesNotInRoom
            AffineTransform scaleMatrix = new AffineTransform();
            scaleMatrix.translate(300, 20 );

            int loopCount = 0;
            for(Pair<Path2D, Float> drawThisPair : drawThisPairs){
                if (loopCount == 30) {
                    scaleMatrix.translate(-1450, 100);
                    loopCount = 0;
                } else {
                    scaleMatrix.translate(50, 0);
                }
                g2d.setTransform(scaleMatrix);
                Path2D furnitureToDraw = drawThisPair.getKey();
                Float rgbValueForFurniture = drawThisPair.getValue();
                g2d.setPaint(new Color(rgbValueForFurniture, rgbValueForFurniture, RGB_Blue_Value));
                g2d.fill(furnitureToDraw);
                g2d.draw(furnitureToDraw);
                loopCount += 1;
            }
        } finally {
            g2d.setTransform(saveTransform);
        }
    }

    private void calculateIntensity(ArrayList<Float> weightages) {
        Float minimum = Collections.min(weightages);
        Float maximum = Collections.max(weightages);
        for(Float weightage : weightages) {
            rgbValues.add((weightage - minimum)/(maximum - minimum));
        }
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        drawFurnitureOutside(g);
    }

}