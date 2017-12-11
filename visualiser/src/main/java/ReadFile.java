import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ReadFile {
    private String room;
    private ArrayList<String> shapesInRoom = new ArrayList<>();
    private ArrayList<String> shapesNotInRoom = new ArrayList<>();
    ReadFile(String filename){
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filename));
            room = reader.readLine();
            String line;
            while(!(line = reader.readLine()).equals("#")){
                shapesInRoom.add(line);
            }
            while((line = reader.readLine())!= null){
                shapesNotInRoom.add(line);
            }
            reader.close();
        }catch(Exception e){
            System.err.printf("There was an error in reading %s", filename);
            e.printStackTrace();
        }
    }

    public String getRoom() {
        return room;
    }

    public ArrayList<String> getShapesInRoom() {
        return shapesInRoom;
    }

    public ArrayList<String> getShapesNotInRoom() {
        return shapesNotInRoom;
    }

}
