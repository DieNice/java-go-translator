package main
import "fmt"

func main() { 
   //Formula3
   var a ,b ,c bool
   a = true 
   b = false 
   c = false 
   c = a || b
   c = a && b
   c = a || b || c
   c = a || b && c
   c = a && b || c
   c = a && b && c
}