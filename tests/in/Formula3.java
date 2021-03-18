public class Formula3 {
    public static void main(String[] args){
        boolean a, b, c;
        a = true;
        b = false;
        c = false;
        c = a || b;
        c = a && b;
        c = a || b || c;
        c = a || b && c;
        c = a && b || c;
        c = a && b && c;
    }
}
