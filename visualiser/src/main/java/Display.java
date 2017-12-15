import java.awt.*;
import java.util.ArrayList;
import javax.swing.*;

public class Display extends JFrame{

        Display(String room, ArrayList<String> shapesInRoom, ArrayList<String> shapesNotInRoom) {
            initUI(room, shapesInRoom, shapesNotInRoom);
        }

        private void initUI(String room, ArrayList<String> shapesInRoom, ArrayList<String> shapesNotInRoom) {
            add(new Room(room, shapesInRoom, shapesNotInRoom));
            setTitle("Visualiser");
            setSize(1920, 1080);
            setLocationRelativeTo(null);
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        }

        public static void main(String[] args) {

            EventQueue.invokeLater(new Runnable() {

                @Override
                public void run() {
                    String filename = "C:\\Users\\zheng\\Desktop\\room_furnishing\\visualiser\\src\\main\\java\\1.txt";
                    ReadFile read = new ReadFile(filename);
                    Display ex = new Display(read.getRoom(), read.getShapesInRoom(), read.getShapesNotInRoom());
                    ex.setVisible(true);
                }
            });
        }
}
