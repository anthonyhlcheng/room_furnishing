

import javafx.util.Pair;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.AffineTransform;
import java.awt.geom.Line2D;
import java.awt.geom.Path2D;
import java.util.ArrayList;
import java.util.Scanner;


class Room extends JPanel {

    private ArrayList<Pair<Double,Double>> coordinates = new ArrayList<>();
    private ArrayList<String> shapesInRoom = new ArrayList<>();
    private ArrayList<String> shapesNotInRoom = new ArrayList<>();
    private static final Double SCALE = 2.0; //PAPER SCALE
    private final Double STARTX = 20.0;
    private final Double STARTY = 20.0;

    Room(String room, ArrayList<String> shapesInRoom, ArrayList<String> shapesNotInRoom){
        //The string room is formatted as follows: (0,0), (0,1), (0,2) and so on...
        StringToCoordinates converter = new StringToCoordinates(room);
        coordinates = converter.getCoordinates();
        this.shapesInRoom = shapesInRoom;
        this.shapesNotInRoom = shapesNotInRoom;
    }
    private void drawRoom(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        AffineTransform saveTransform = g2d.getTransform();
        ShapeGenerator generator = new ShapeGenerator();
        generator.create(coordinates);
        Path2D room = generator.getPaths().get(0);

        //Place furniture in room
        ShapeGenerator furnitureGenerator = new ShapeGenerator(shapesInRoom);
        ArrayList<Path2D> furnitures = furnitureGenerator.getPaths();
        //Scales the room to our needs
        try {
            AffineTransform scaleMatrix = new AffineTransform();
            scaleMatrix.translate(STARTX-generator.minX,STARTY-generator.minY);
            scaleMatrix.scale(SCALE, SCALE);
            g2d.setTransform(scaleMatrix);

            //Colouring in the furniture inside the room
            for(Path2D furniture:furnitures){
                int R = (int)(25 + (Math.random() * ((255-25) + 1)));
                int G = (int)(25 + (Math.random() * ((255-25) + 1)));
                int B = (int)(25 + (Math.random() * ((255-25) + 1)));
                int borderOffset = 20;
                g2d.setPaint(new Color(R,G,B));
                g2d.fill(furniture);
                g2d.setPaint(new Color(R-borderOffset, G-borderOffset, B-borderOffset));
                g2d.setStroke(new BasicStroke(1.0f));
                g2d.draw(furniture);
            }

            g2d.setPaint(Color.BLACK);
            float thickness = 2.0f;
            Stroke oldStroke = g2d.getStroke();
            g2d.setStroke(new BasicStroke(thickness));
            g2d.draw(room);
            g2d.setStroke(oldStroke);

        } finally {
            g2d.setTransform(saveTransform);
        }

        ColorIntensity colorIntensity = new ColorIntensity(shapesNotInRoom);
        colorIntensity.paintComponent(g2d);
    }

    public ArrayList<Pair<Double, Double>> getCoordinates() {
        return coordinates;
    }

    @Override
    public void paintComponent(Graphics g) {

        super.paintComponent(g);
        drawRoom(g);
    }
}