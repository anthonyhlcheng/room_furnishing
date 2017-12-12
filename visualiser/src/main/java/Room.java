

import javafx.util.Pair;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.geom.Line2D;
import java.awt.geom.Path2D;
import java.util.ArrayList;
import java.util.Scanner;


class Room extends JPanel {

    private ArrayList<Pair<Double,Double>> coordinates = new ArrayList<>();
    private ArrayList<String> shapesInRoom = new ArrayList<>();
    private static final Double SCALE = 1.0; //PAPER SCALE
    private final Double STARTX = 20.0;
    private final Double STARTY = 20.0;

    Room(String room, ArrayList<String> shapesInRoom){
        //The string room is formatted as follows: (0,0), (0,1), (0,2) and so on...
        StringToCoordinates converter = new StringToCoordinates(room);
        coordinates = converter.getCoordinates();
        this.shapesInRoom = shapesInRoom;
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
            g2d.draw(room);

            //Colouring in the furniture inside the room - this is only an example
            for(Path2D furniture:furnitures){
                g2d.setPaint(Color.BLACK);
                g2d.fill(furniture);
                g2d.draw(furniture);
            }
        } finally {
            g2d.setTransform(saveTransform);
        }
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