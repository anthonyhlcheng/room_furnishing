

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
    private Double minX = -50.0;
    private Double minY = -50.0;
    private static final Double SCALE = 10.0;
    private static final Double STARTX = 50.0;
    private static final Double STARTY = 50.0;

    Room(String room){
        //The string room is formatted as follows: (0,0), (0,1), (0,2) and so on...
        room = room.replace(" ","").replace("),(", ")/(");
        String[] coordinateArray = room.split("/");
        for(String coordinate:coordinateArray){
            System.out.println(coordinate);
            int commaLocation = coordinate.indexOf(",");
            Double x = Double.parseDouble(coordinate.substring(1,commaLocation));
            Double y = Double.parseDouble(coordinate.substring(commaLocation+1, coordinate.length()-1));
            if(x < minX){
                minX = x;
            }
            if(y < minY){
                minY = y;
            }
            coordinates.add(new Pair<>(x,y));
        }
    }
    private void drawRoom(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        AffineTransform saveTransform = g2d.getTransform();
        Path2D room = new Path2D.Double();
        boolean isFirst = true;
        for(Pair<Double,Double> pair:coordinates){
            Double x = pair.getKey();
            Double y = pair.getValue();
            if(isFirst) {
                room.moveTo(x,y);
                isFirst = false;
            }else{
                room.lineTo(x,y);
            }

        }
        room.closePath();
        //Scales the room to our needs
        try {
            AffineTransform scaleMatrix = new AffineTransform();
            scaleMatrix.translate(STARTX,STARTY);
            scaleMatrix.scale(SCALE, SCALE);
            g2d.setTransform(scaleMatrix);
            g2d.draw(room);
        } finally {
            g2d.setTransform(saveTransform);
        }
    }

    public ArrayList<Pair<Double, Double>> getCoordinates() {
        return coordinates;
    }

    public ArrayList<Float> getWeightages(ArrayList<String> shapesNotInRoom) {
        ArrayList<Float> weightage = null;
        for(String shape : shapesNotInRoom) {
            String[] splitted = shape.split(":");
            weightage.add(Float.parseFloat(splitted[0]));
        }
        return weightage;
    }

    @Override
    public void paintComponent(Graphics g) {

        super.paintComponent(g);
        drawRoom(g);
    }
}