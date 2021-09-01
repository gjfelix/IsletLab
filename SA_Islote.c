/*
 * SA_Islote_tol_Paralelo.c
 *
 *  Created on: 14 abr. 2020
 *      Author: gjfelix modificado por Aurelio
 *  Compile: gcc SA_Islote_tol_Paralelo_omp.c -o SA_Islote_Tol_H51 -lm -fopenmp
 *  run ./SA_Islote_Tol_H51
 */

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <omp.h>

time_t rawtime;
struct tm * timeinfo;


// Numero de celulas en archivo de Islote
#define numCells 588
#define NUMHILOS 20

//struct islote{
//	int n_celula;
//	double tipo_celula;
//	double coordx;
//	double coordy;
//	double coordz;
//};

//struct isloteH51 islote[numCells];

// Arreglo para guardar archivo de Islote
double isloteinicial[numCells][4];
double isloteactual[numCells][4];
double islotefinal[numCells][4];

double colorcells[numCells];

// Arreglo para guardar distancias entre celulas
double distNucMatriz[numCells][numCells];

// Arreglo para guardar radios de celulas
double radiosCelulas[numCells];
double radiosCelulasFinal[numCells];

// Arreglo para guardar suma de radios
double sumaRadiosMatriz[numCells][numCells];

double new_rCells[numCells];
double new_islote[numCells][4];
double new_sumaRadiosMatriz[numCells][numCells];
double new_distNucMatriz[numCells][numCells];

double e = 0; //energia
omp_lock_t c_e; //declaracion de un candado c_e

int cumpleCondicion = 0;
int condicion1 = 0;
int condicion2 = 0;
// Procedimiento para cargar archivo de Hoang
// 4 columnas: Col1: TipoCelula, Col2: X, Col3: Y, Col4: Z
void cargarArchivo() {
	FILE *fp;
	int numcelula = 0;
	fp = fopen("H51.txt", "r");
	//fp = fopen("testData.txt", "r");
	char linea[1000000];
	while (fgets(linea, sizeof(linea), fp)) {
		char *p = strtok(linea, " ");
		int j = 0;
		while (p != NULL) {
			//printf( " %s\t", p );
			double a = atof(p);
			isloteinicial[numcelula][j] = a;
			isloteactual[numcelula][j] = a;
			islotefinal[numcelula][j] = a;
			p = strtok(NULL, " ");
			j++;
		}
		numcelula++;
	}
}

// Funcion para calcular el cuadrado de algo (para distancias)
double square(double Number) {
	return Number * Number;
}

void distNucleos(double coordNucleos[numCells][4],
		double distNucMatriz[numCells][numCells]) {
	int i;
	int j;
	for (i = 0; i < numCells; i++) {
		for (j = 0; j < numCells; j++) {
			distNucMatriz[i][j] = sqrt(
					square((coordNucleos[i][1] - coordNucleos[j][1]))
							+ square((coordNucleos[i][2] - coordNucleos[j][2]))
							+ square(
									(coordNucleos[i][3] - coordNucleos[j][3])));
		}
	}
}

// Funcion para generar numeros aleatorios con distribucion normal
double rand_normal(double mean, double stddev) { //Box muller method
	static double n2 = 0.0;
	static int n2_cached = 0;
	if (!n2_cached) {
		double x, y, r;
		do {
			x = 2.0 * rand() / RAND_MAX - 1;
			y = 2.0 * rand() / RAND_MAX - 1;

			r = x * x + y * y;
		} while (r == 0.0 || r > 1.0);
		{
			double d = sqrt(-2.0 * log(r) / r);
			double n1 = x * d;
			n2 = y * d;
			double result = n1 * stddev + mean;
			n2_cached = 1;
			return result;
		}
	} else {
		n2_cached = 0;
		return n2 * stddev + mean;
	}
}

// // Funcion para generar radios de celulas con base en tipo de celula
// void generarRadios(double dataislote[numCells][4], double radios[numCells]) {
// 	int i;
// 	for (i = 0; i < numCells; i++) {
// 		if (dataislote[i][0] == 12.0) {
// 			radios[i] = rand_normal(6.49, 1.6);
// 			if(radios[i]<4.48){
// 				radios[i] = 4.48 - radios[i] + 4.48;
// 			} else if(radios[i]>8.21) {
// 				radios[i] =  8.21 - radios[i] + 8.21;
// 			}
// 		} else if (dataislote[i][0] == 11.0) {
// 			radios[i] = rand_normal(5.04, 0.9);
// 			if(radios[i]<4.33){
// 				radios[i] = 4.33 - radios[i] + 4.33;
// 			} else if(radios[i]>6.84) {
// 				radios[i] =  6.84 - radios[i] + 6.84;
// 			}
// 		} else {
// 			radios[i] = rand_normal(5.6, 0.9);
// 			if(radios[i]<4.39){
// 				radios[i] = 4.39 - radios[i] + 4.39;
// 			} else if(radios[i]>6.92) {
// 				radios[i] =  6.92 - radios[i] + 6.92;
// 			}
// 		}
// 	}
// }

void generarRadios(double dataislote[numCells][4], double radios[numCells]){
	int i;
	for(i = 0; i < numCells; i++){
		if(dataislote[i][0] == 12.0){
			radios[i] = rand_normal(6.49, 1.6);
			while(radios[i]<4.48 || radios[i] > 8.21 ){
				radios[i] = rand_normal(6.49, 1.6);
			}	
		} else if(dataislote[i][0] == 11.0){
			radios[i] = rand_normal(5.04, 0.9);
			while(radios[i]<4.33 || radios[i] > 6.84 ){
				radios[i] = rand_normal(5.04, 0.9);
			}
		} else {
			radios[i] = rand_normal(5.6, 0.9);
			while(radios[i]<4.39 || radios[i] > 6.92 ){
				radios[i] = rand_normal(5.6, 0.9);
			}
		}
	}
}

double generarRadio(double tipoCelula) {
	double radio;
	if (tipoCelula == 12.0) {
		radio = rand_normal(6.49, 1.6);
		while(radio<4.48 || radio > 8.21 ){
				radio = rand_normal(6.49, 1.6);
			}
		
	} else if (tipoCelula == 11.0) {
		radio = rand_normal(5.04, 0.9);
		while(radio<4.33 || radio > 6.84 ){
				radio = rand_normal(5.04, 0.9);
			}
	} else {
		radio = rand_normal(5.6, 0.9);
		while(radio<4.39 || radio > 6.92 ){
				radio = rand_normal(5.6, 0.9);
			}
	}
	return radio;
}

// double generarRadio(double tipoCelula) {
// 	double radio;
// 	if (tipoCelula == 12.0) {
// 		radio = rand_normal(6.49, 1.6);
// 		if(radio<4.48){
// 				radio = 4.48 - radio + 4.48;
// 			} else if(radio>8.21) {
// 				radio =  8.21 - radio + 8.21;
// 			}
// 	} else if (tipoCelula == 11.0) {
// 		radio = rand_normal(5.04, 0.9);
// 		if(radio<4.33){
// 				radio = 4.33 - radio + 4.33;
// 			} else if(radio>6.84) {
// 				radio =  6.84 - radio + 6.84;
// 			}
// 	} else {
// 		radio = rand_normal(5.6, 0.9);
// 		if(radio<4.39){
// 				radio = 4.39 - radio + 4.39;
// 			} else if(radio>8.21) {
// 				radio =  6.92 - radio + 6.92;
// 			}
// 	}
// 	return radio;
// }

void sumaRadios(double radios[numCells],
		double sumaRadiosMatriz[numCells][numCells]) {
	int i;
	int j;
	for (i = 0; i < numCells; i++) {
		for (j = 0; j < numCells; j++) {
			sumaRadiosMatriz[i][j] = radios[i] + radios[j];
		}
	}
}

// Funcion para generar numero aleatorio uniforme entre M y N
double randMToN(double M, double N) {
	return M + (rand() / ( RAND_MAX / (N - M)));
}

double randzerotoone() {
	return (double) rand() / (double) RAND_MAX;
}

void moverRadioNucleo() {
	double minmove, maxmove;
	int j;
	// Selecciono celula a mover
	int randomcell = rand() % numCells;
	// Genero radio nuevo
	new_rCells[randomcell] = generarRadio(isloteactual[randomcell][0]);
	// Selecciono direccion para mover nucleo
	int dirmov = rand() % 3 + 1;
	// Calculo nueva coordenada
	minmove = isloteinicial[randomcell][dirmov] - new_rCells[randomcell];
	maxmove = isloteinicial[randomcell][dirmov] + new_rCells[randomcell];
	for (j = 0; j < 4; j++) {
		new_islote[randomcell][j] = isloteinicial[randomcell][j];
	}
	new_islote[randomcell][dirmov] = randMToN(minmove, maxmove);
}

void guardarArchivoFinal(double radiosCelulasFinal[numCells],
		double color[numCells]) {
	int i, j;
	FILE *archivoSalida = fopen("isloteFinal.txt", "w");
	for (j = 0; j < numCells; ++j) {
		fprintf(archivoSalida, "%lf\t%lf\t", radiosCelulasFinal[j], color[j]);
		for (i = 0; i < 4; ++i) {
			fprintf(archivoSalida, "%lf\t", islotefinal[j][i]);
		}
		fprintf(archivoSalida, "\n");
	}
	fclose(archivoSalida);
}

void guardarArchivoInicial(double radiosCelulas[numCells],
		double color[numCells]) {
	int i, j;
	FILE *archivoSalida = fopen("isloteInicial.txt", "w");
	for (j = 0; j < numCells; ++j) {
		fprintf(archivoSalida, "%lf\t%lf\t", radiosCelulas[j], color[j]);
		for (i = 0; i < 4; ++i) {
			fprintf(archivoSalida, "%lf\t", isloteinicial[j][i]);
		}
		fprintf(archivoSalida, "\n");
	}
	fclose(archivoSalida);
}

// Funcion para calcular energia
double energia(double matrizSumaRadios[numCells][numCells],
		double matrizDistancias[numCells][numCells]) {
	int i;
	int j;
	for (i = 0; i < numCells; i++) {
		for (j = i+1; j < numCells; j++) {
			if (matrizSumaRadios[i][j] > matrizDistancias[i][j]) {
				e = e + 1;
			}
		}
	}
	return (double) e;
}

// Funcion para calcular energia
void energiaLoop() {
	int i;
	int j;
	for (i = 0; i < numCells; i++) {
		for (j = 0; j < numCells; j++) {
			if (new_sumaRadiosMatriz[i][j] > new_distNucMatriz[i][j]) {

				omp_set_lock(&c_e); //Operacion equivalente a Lock, para cerrar un candado
				e = e + 1;
				omp_unset_lock(&c_e); //Operacion equivalente a unlock, para abrir un candado
			}
		}
	}
}

// Funciones para obtener maximo y minimo
double max(double num1, double num2) {
	return (num1 > num2) ? num1 : num2;
}

double min(double num1, double num2) {
	return (num1 > num2) ? num2 : num1;
}

/*double dEmax(double Eini, int niter, double radiosCelulas[numCells], double islote[numCells][4],
 double distNucMatriz[numCells][numCells], double sumaRadiosMatriz[numCells][numCells]){
 double maxdE =0;
 double dE;
 int i;
 double temp;
 for(i=0; i<niter; i++){
 moverRadioNucleo();
 distNucleos(islote, distNucMatriz);
 sumaRadios(radiosCelulas, sumaRadiosMatriz);
 dE = fabs(Eini - energia(sumaRadiosMatriz, distNucMatriz));
 if(dE>maxdE){
 maxdE = dE;
 }
 }
 return maxdE;

 }*/

void celcolor(double islote[numCells][4], double col[numCells]) {
	int i;
	for (i = 0; i < numCells; i++) {
		if (islote[i][0] == 11.0) {
			col[i] = 1.0;
		} else if (islote[i][0] == 12.0) {
			col[i] = 0.4;
		} else {
			col[i] = 0.6;
		}
	}
}

int main(void) {
	time_t begin = time(NULL);
	srand(time(NULL));
	int MaxTrialN = numCells * 1000; // 500;
	int MaxAcceptN = numCells * 500; //100;
	double StopTolerance = 0.001;
	double TempRatio = 0.5;
	double minE = INFINITY;
	double maxE = -1;
	//double temp = 60.0;
	int TrialN;
	int AcceptN;
	int newE;
	int j;
	double temp;
	double E;
	FILE *archivoLog = fopen("ProcessLog.txt", "w");
	fprintf(archivoLog, "%-9s\t%-10s\t%-10s\t%-10s\t%-4s\t%-4s\t%s\n", "temp", "E", "minE", "maxE", "AcceptN", "TrialN","Time");

	omp_init_lock(&c_e); //el candado queda abierto por default
	omp_unset_lock(&c_e); //CANDADO DE e ABIERTO

	cargarArchivo();
	// Se guarda isloteinicial, isloteactual, islotefinal (arreglos con 4 columnas y numCells renglones)
	// Para probar carga de archivo
	//int i;
	//for(i=0; i<numCells; i++){
	//	printf("Celula %d: %lf, %lf, %lf, %lf\n", i, islote[10][0],
	//			islote[i][1], islote[i][2], islote[i][3]);
	//};

	// Arreglo 1D para guardar colores de celulas para visualizacion
	celcolor(isloteinicial, colorcells);
	// Arreglo 2D para matriz de distancia entre nucleos

	/******************************************************************************
	 /******************************************************************************
	 /******************************************************************************
	 /******************************************************************************
	 double distNucMatriz[numCells][numCells];
	 ********************************************************************************/
	// Calculo matriz de distancia entre nucleos de islote inicial
	distNucleos(isloteinicial, distNucMatriz);

	// Para probar generacion de matriz de distancias
	//int i, j;
//	for (i = 0; i < numCells; i++) {
//		for (j = 0; j < numCells; j++) {
//			printf("%f\t", distNucMatriz[i][j]);
//		}
//		printf("\n");
//	}

	// Arreglo 1D para radios de celulas

	/******************************************************************************
	 /******************************************************************************
	 /******************************************************************************
	 /******************************************************************************
	 double radiosCelulas[numCells];
	 ********************************************************************************/
	// Genero radios iniciales
	generarRadios(isloteinicial, radiosCelulas);
	// Pruebo calculo de radios con funcion generarRadios();
	//int i;
//	for (i = 0; i < numCells; i++) {
//		printf("R%d = %lf\n", i, radiosCelulas[i]);
//	};

	// Pruebo generar radios uno por uno con funcion generarRadio();
//	int i;
//	for(i=0; i<numCells; i++){
//		printf("R%d = %lf\n", i, generarRadio(islote[i][0]));
//	};

	// Arreglo 2D para suma de radios

	/******************************************************************************
	 /******************************************************************************
	 /******************************************************************************
	 /******************************************************************************

	 double sumaRadiosMatriz[numCells][numCells];

	 ********************************************************************************/

	// Calculo matriz de suma de radios con radios iniciales
	sumaRadios(radiosCelulas, sumaRadiosMatriz);
	// Pruebo generar matriz de suma de radios

//	for (i = 0; i < numCells; i++) {
//		for (j = 0; j < numCells; j++) {
//			printf("%f\t", sumaRadiosMatriz[i][j]);
//		}
//		printf("\n");
//	}

	// Pruebo funcion para calcular energia

	// Calculo energia inicial
	E = energia(sumaRadiosMatriz, distNucMatriz);
	printf("\nEnergia calculada: %f\n", E);
	fflush(stdout);
//	for (i = 0; i < numCells; i++) {
//		for (j = 0; j < numCells; j++) {
//			if (sumaRadiosMatriz[i][j] > distNucMatriz[i][j]) {
//				printf("%d \t", 1);
//			} else {
//				printf("%d \t", 0);
//			}
//
//		}
//		printf("\n");
//	}

	guardarArchivoInicial(radiosCelulas, colorcells);

	//Pruebo mover radio y nucleo
	// Imprimo islote actual antes de movimiento
//	int i;
//	for (i = 0; i < numCells; i++) {
//		printf("Celula %d: %lf, %lf, %lf, %lf, %lf\n", i, radiosCelulas[i], isloteactual[i][0],
//				isloteactual[i][1], isloteactual[i][2], isloteactual[i][3]);
//	};
	//moverRadioNucleo(radiosCelulas, isloteactual, isloteinicial);
	// Imprimo islote actual despues de movimiento

//	for (i = 0; i < numCells; i++) {
//			printf("Celula %d: %lf, %lf, %lf, %lf, %lf\n", i, radiosCelulas[i], isloteactual[i][0],
//					isloteactual[i][1], isloteactual[i][2], isloteactual[i][3]);
//		};
//	int dEmax;
//	dEmax = maxdE(E, 50, radiosCelulas, isloteinicial,distNucMatriz, sumaRadiosMatriz);
//	temp = (double)(dEmax*10);
//	printf("dEmax = %d, Temperatura inicial = %f\n", dEmax, temp);
	temp = 100.0;
	//fprintf(archivoLog, "%s\t%s\t%s\t%s\t%s\t%s\n", "Temp", "E", "minE", "maxE",
	//		"AcceptN", "TrialN");

	int id, id_aux;
	omp_set_num_threads(NUMHILOS);
#pragma omp parallel private(id,id_aux,j) shared(isloteinicial, isloteactual, islotefinal, colorcells, distNucMatriz, radiosCelulas, radiosCelulasFinal, sumaRadiosMatriz, new_rCells, new_islote, new_sumaRadiosMatriz, new_distNucMatriz, e, c_e, cumpleCondicion, condicion1, condicion2,MaxTrialN,MaxAcceptN,StopTolerance,TempRatio,minE,maxE,TrialN,AcceptN,newE,temp,E)
	{

		id = omp_get_thread_num();

		fprintf(stdout, "Hola soy %d\n",id);
		if (id == 0) {
			if ((maxE - minE) / maxE > StopTolerance) {
				condicion1 = 1;
			}
		}

#pragma omp barrier

		while (condicion1 == 1) {
			//printf("condicion = %f\n", (double)(maxE - minE)/maxE);
			if (id == 0) {
				minE = INFINITY;
				maxE = 0;
				TrialN = 0;
				AcceptN = 0;
				if (TrialN < MaxTrialN && AcceptN < MaxAcceptN) {
					condicion2 = 1;
				}
			}

#pragma omp barrier
			while (condicion2 == 1) {
				//printf("%d\n", TrialN);
				//Copio radios aceptados y coordenadas aceptadas

				id_aux = id;

				while (id_aux < numCells) {

					new_rCells[id_aux] = radiosCelulas[id_aux];

					for (j = 0; j < 4; j++) {
						new_islote[id_aux][j] = islotefinal[id_aux][j];
					}

					id_aux = id_aux + NUMHILOS;
				}

#pragma omp barrier

				// Muevo radio en new_radiosCelulas
				// y coordenadas de nucle en islote actual
				if (id == 0) {
					moverRadioNucleo();
				}
#pragma omp barrier
				id_aux = id;
				while (id_aux < numCells) {
					// Creo nueva matriz de suma de radios
					for (j = id_aux + 1; j < numCells; j++) {
						new_sumaRadiosMatriz[id_aux][j] = new_rCells[id_aux]
								+ new_rCells[j];

						// Creo nueva matriz de distancia de nucleos
						new_distNucMatriz[id_aux][j] = sqrt(
								square(
										(new_islote[id_aux][1]
												- new_islote[j][1]))
										+ square(
												(new_islote[id_aux][2]
														- new_islote[j][2]))
										+ square(
												(new_islote[id_aux][3]
														- new_islote[j][3])));
					}
					id_aux = id_aux + NUMHILOS;
				}

				if (id == 0) {
					e = 0;
					cumpleCondicion = 0;

				}

#pragma omp barrier

				//distNucleos(isloteactual, distNucMatriz);
				//sumaRadios(new_radiosCelulas, sumaRadiosMatriz);

				//calcular energia
				id_aux = id;
				while (id_aux < numCells) {
					for (j = id_aux + 1; j < numCells; j++) {
						if (new_sumaRadiosMatriz[id_aux][j]
								> new_distNucMatriz[id_aux][j]) {
							omp_set_lock(&c_e); //Operacion equivalente a Lock, para cerrar un candado
							//printf("Hola soy %d leo\te = %lf\n",id,e);
							e = e + 1;
							//printf("Hola soy %d escribo\te = %lf\n",id,e);
							omp_unset_lock(&c_e); //Operacion equivalente a unlock, para abrir un candado
						}
					}
					id_aux = id_aux + NUMHILOS;
				}
#pragma omp barrier
				if (id == 0) {
					TrialN = TrialN + 1;
					newE = e;
					if (randzerotoone() < ((double) exp((E - newE) / temp))) {
						cumpleCondicion = 1;
						E = newE;
						minE = min(minE, E);
						maxE = max(maxE, E);
						AcceptN = AcceptN + 1;
					//	for(i = 0; i < numCells; i++){
					//		radiosCelulas[i] = new_rCells[i];
					//		for(j = 0; j < 4; j++){
					//			islotefinal[i][j] = new_islote[i][j];
					//		}
					//	}
					}
				}

#pragma omp barrier

				//printf("E = %d, newE = %d\n", E, newE);
				if (cumpleCondicion == 1) {
					// Copio radios e islotes aceptados en arreglos finales
					id_aux = id;
					while (id_aux < numCells) {
						radiosCelulas[id_aux] = new_rCells[id_aux];
						for (j = 0; j < 4; j++) {
							islotefinal[id_aux][j] = new_islote[id_aux][j];
						}
						id_aux = id_aux + NUMHILOS;
					}
				}

				if (id == 0) {
					if (TrialN < MaxTrialN && AcceptN < MaxAcceptN) {
						condicion2 = 1;
					} else {
						condicion2 = 0;
					}
				}
#pragma omp barrier
			}
			if (id == 0) {

				  time(&rawtime);
				  timeinfo = localtime(&rawtime);
				  //printf ( "Current local time and date: %s", asctime (timeinfo) );

				fprintf(archivoLog, "%lf\t%lf\t%lf\t%lf\t%d\t%d\t%s", temp, E,
						minE, maxE, AcceptN, TrialN, asctime(timeinfo));
				fflush(archivoLog);
				printf("temp = %f\n", temp);
				fflush(stdout);
				printf("energy = %f\n", E);
				printf("[minE maxE] = [%f %f]\n", minE, maxE);
				printf("[AcceptN TrialN] = [%d %d]\n\n", AcceptN, TrialN);
				//printf("Tiempo de iteracion: %f \n\n", cpu_time_used);
				temp = temp * TempRatio;

				if ((double) (maxE - minE) / maxE > StopTolerance) {
					condicion1 = 1;
				} else {
					condicion1 = 0;
				}
			}
#pragma omp barrier
			guardarArchivoFinal(radiosCelulas, colorcells);
		}
	}
	fclose(archivoLog);
	//guardarArchivoFinal(radiosCelulas, colorcells);

	time_t end = time(NULL);
	printf("Tiempo de ejecucion: %ld segundos\n", (end - begin));
	return 0;
}

