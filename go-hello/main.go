package main

import (
	"fmt"
	"runtime"
	"time"
)

func main() {
	fmt.Println("==================================================")
	fmt.Println("🚀 SETUP COMPLETO - GO!")
	fmt.Println("==================================================")
	fmt.Printf("\nData: %s\n", time.Now().Format("02/01/2006"))
	fmt.Printf("Go: %s\n", runtime.Version())
	fmt.Println("\n✅ Pronto para Semana 1, Dia 1!")
	fmt.Println("==================================================")
}