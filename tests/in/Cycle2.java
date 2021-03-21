public class Cycle2 {
    public static void main(String[] args){
        int a;
        a = 0;
        for (int i = 0; i < 10; i++){
            a = a + 100;
            for (int j = 0; j < 10; j++){
                a = a + 10;
            };
        };
    }
}
