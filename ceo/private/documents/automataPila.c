/*
Instituto Politécnico Nacional
Escuela Superior de Computación

Alumno: Ramirez Hidalgo Marco Antonio
Materia: Teoría computacional
Docente: Benjamin Luna Benoso
Grupo: 2CV1

Implementación de un AP determinista

Sabado, 26 de diciembre del 2020.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AP.h"
#include "archivo.h"
#define CAD 100

int main()
{
	int n, i = 0, cargadoAP = 0, opcionAP = 0, opc1, opc2;
	FILE *registro = fopen("registros.txt", "r");
	
	//Se obtienen la cantidad de configuraciones registradas
	n = cantidadConfig(registro);
	
	if(n == 0)
		return 1;
		
	int apAbierto[n];
	char **configs = (char **) malloc(sizeof(char *) * n);
	AP automata[n];
	char *cadena = (char *) malloc(sizeof(char) * CAD + 1);
	
	rewind(registro);	
	
	//Se recuperan los nombres de los archivos que tienen una configuracion
	while(!feof(registro))
	{
		configs[i] = leerLineaAP(registro);
		i++;
	}
	
	fclose(registro);
	
	for(i = 0; i < n; i++)
		apAbierto[i] = 0;
	
	do
	{
		printf("\nM E N U   P R I N C I P A L\n\n");
		cargadoAP ? printf("\tAP - %s\n\n", configs[opcionAP - 1]) : printf("\tAun no se carga ningun AP\n\n");
		printf("\tOpciones\n");
		printf("\t\t1. Cargar AP");
		printf("\n\t\t2. Probar AP");
		printf("\n\t\t3. Salir");
		printf("\n\tEscoger opcion: ");
		scanf("%d", &opc1);
		
		system("cls");
		switch(opc1)
		{
			case 1:
				
				do
				{
					printf("\nM E N U   C A R G A R   A P\n\n");
					
					printf("\tOpciones\n");
					for(i = 0; i < n; i++)
						printf("\t\t%03d. %s\n", i + 1, configs[i]);
				
					printf("\tEscoger opcion: ");
					scanf("%d", &opcionAP);
					
					if(opcionAP < 1 || opcionAP > n)
					{
						printf("\n\tOpcion invalida\n\t");
						system("pause");
					}
					
				} while (opcionAP < 1 || opcionAP > n);
				
				if(!cargadoAP)
					cargadoAP = 1;
				
				//Se determina si una configuracion ya fue abierta para no volverla a cargar en el arreglo. En cao contrario, se carga la configuracion
				if(!apAbierto[opcionAP - 1])
				{
					automata[opcionAP - 1] = extraerAp(configs[opcionAP - 1]);
					apAbierto[opcionAP - 1] = 1;
				}
				
				break;
			case 2:
				
				if(!cargadoAP)
				{
					printf("\nNo hay ningun AP cargado\n");
					system("pause");
					break;
				}
				
				do
				{
					printf("\nM E N U   P R O B A R   A P\n\n");
					
					printf("\tAutomata a pila - %s", configs[opcionAP - 1]);
					
					printf("\n\tAlfabeto de entrada: ");
					ImpSimbolos(getAlfabetoE(automata[opcionAP - 1]));
					printf("\n\tAlfabeto de pila: ");
					ImpSimbolos(getAlfabetoP(automata[opcionAP - 1]));
					
					printf("\n\n\tOpciones");
					printf("\n\t\t1. Ingresar cadena");
					printf("\n\t\t2. Salir\n");
					printf("\tEscoger opcion: ");
					scanf("%d", &opc2);
					
					if(opc2 < 1 || opc2 > 2)
					{
						printf("\n\tOpcion invalida\n\t");
						system("pause");
					}
					
					if(opc2 == 2)
						break;
					
					if(opc2 == 1)
					{
						fflush(stdin);
						printf("\n\tDigita la cadena: ");
						fgets(cadena, CAD + 1, stdin);
						
						printf("\n\tTraza de ejecucion: \n\n\t  ");
						if(trazaEjecucion(cadena, automata[opcionAP - 1]))
							printf("\n\tCADENA ACEPTADA\n\n");
						else
							printf("\n\tCadena NO aceptada\n\n\t");
						
						system("pause");
						
					}
					system("cls");
				} while (opc2 <= 1 || opc2 > 2);				
				
				break;
		}
		system("cls");
	} while(opc1 != 3);
	
	for(i = 0; i < n; i++)
		free(configs[i]);
	
	free(configs);
	free(cadena);
	
	fclose(registro);
	
	return 0;
}
