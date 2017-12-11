

import javafx.util.Pair;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.Line2D;
import java.util.ArrayList;
import java.util.Scanner;


class Room extends JPanel {

    private ArrayList<Pair<Double,Double>> coordinates = new ArrayList<>();
    private Double minX = -50.0;
    private Double minY = -50.0;
    private int scaler = 50;
    Room(String room){
        //The string room is formatted as follows: (0,0), (0,1), (0,2) and so on...
        String[] coordinateArray = room.trim().split(", ");
        for(String coordinate:coordinateArray){
            System.out.println(coordinate);
            int commaLocation = coordinate.indexOf(",");
            Double x = Double.parseDouble(coordinate.substring(1,commaLocation));
            Double y = Double.parseDouble(coordinate.substring(commaLocation + 1, coordinate.length()-1));
            if(x < minX){
                minX = x;
            }
            if(y < minY){
                minY = y;
            }
            coordinates.add(new Pair<>(x,y));
        }
        coordinates.add(coordinates.get(0));
    }
    private void drawRoom(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        Double lastX = null;
        Double lastY = null;
        for(Pair<Double,Double> pair:coordinates){
            if(lastX == null || lastY == null) {
                lastX = pair.getKey();
                lastY = pair.getValue();
            }else{
                Double x = pair.getKey();
                Double y = pair.getValue();
                g2d.draw(new Line2D.Double(lastX-minX,lastY-minY,x-minX,y-minY));
                lastX = x;
                lastY = y;
            }
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