/*
 ;
 Name        : kuramoto_islets.cu
 Author      : Gerardo J. Felix-Martinez
 Version     : 0.0
 Copyright   : Your copyright notice
 Description : Implementacion de modelo de Kuramoto para sincronizacion de celulas en los islotes
 
 Graficar en gnuplot: plot for [col=2:4] 'AngulosIslote.data' using 1:col with lines

 */

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


// Parametros globales modelo
#define totalCelulas 514
#define maxVecinos 10 // maximo numero de vecinos por celula
double *Angulos_Device;
double *Angulos_Host;
#define PI 3.14159265358979323846
//#define beta 0.23


// Parametros CUDA
const int numBlocks = 30;
const int threadsPerBlock = 64;
__const__ int NUMHILOS = numBlocks * threadsPerBlock;

struct contactos{
    int id_vecino; // Identificador de vecino en el islote
    double gacople; 
};

struct redcelulas {
    int n_celula;
    int n_vecinos;
    int tipo_celula;
    int id_vecinos[maxVecinos];
    int ind_arreglo_tipo; //identificador en su poblacion
    struct contactos vecinos[maxVecinos];
    double frec;
    double theta;
    double termino_acople;
};

__device__ struct redcelulas islote[totalCelulas];

// Generador de numeros aleatorios con distribucion uniforme
double get_random() { return ((double)rand() / (double)RAND_MAX); }


// Runge Kutta 4to orden
__device__ double rk4(double (*f)(double, int), double h, double x, int i) {
    double k1 = h * f(x, i);
    double k2 = h * f(x + k1 / 2, i);
    double k3 = h * f(x + k2 / 2, i);
    double k4 = h * f(x + k3, i);
    return x + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
}

__global__ void set_TipoCelula(int i, int tipo) {
    // Guarda el tipo de celula que es la celula i
    islote[i].tipo_celula = tipo;

}
__global__ void set_idVecino(int i, int index, int idVecino) {
    // Guarda el id del vecino index de la celula i
    islote[i].id_vecinos[index] = idVecino;

}
__global__ void set_numVecinos(int i, int numvecinos) {
    // Guarda el numero total de vecinos que tiene la celula i
    islote[i].n_vecinos = numvecinos;
}

__global__ void set_idVecinoStruct(int i, int j, int numvecinos){
    islote[i].vecinos[numvecinos].id_vecino = j;
}


// Se calcula termino de acople
__device__ void calcular_acople(int i){
    int j;
    double sum_acoples = 0.0;
    // j itera sobre el numero de vecinos de la celula i
    for (j = 0; j < maxVecinos; j++){
        if (islote[i].id_vecinos[j] >= 0.0){
            sum_acoples = sum_acoples + islote[i].vecinos[j].gacople * sin(islote[islote[i].id_vecinos[j]].theta - islote[i].theta);
            //sum_acoples = sum_acoples + sin(islote[islote[i].id_vecinos[j]].theta - islote[i].theta);
        }
    }
    islote[i].termino_acople = sum_acoples;
    //printf("Celula %i, acople = %f\n", i, islote[i].termino_acople);
}

// Ecuacion diferencial modelo de Kuramoto
__device__ double dthetadt(double theta0, int i){
    //return islote[i].frec + islote[i].termino_acople;
    return islote[i].frec + 1.0/totalCelulas * islote[i].termino_acople;
    //return islote[i].frec + kappa/totalCelulas * islote[i].termino_acople;
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


void cargarArchivo() {
    FILE *fp;
    int i = 0;
//  fp = fopen("conectividad_a_b_d.txt", "r");
    
fp = fopen("/home/gerardo/Documents/IsletLab/H51_all_contacts.txt" ,"r");

    char linea[1000000];
    while (fgets(linea, sizeof(linea), fp)) {
        int numvecinos = 0;
        char *p = strtok(linea, " ");
        int j = 0;
        while (p != NULL) {
            //printf( " %s\t", p );
            int a = atoi(p);
            if (i == j) {
                // guarda tipo de celula de la celula i
                set_TipoCelula<<<1, 1>>>(i, a);
                cudaDeviceSynchronize();
                // Para guardar el id del vecino numvecinos j de la celula i
                // como hay interacciones autocrinas se guarda la celula como su 
                // propia vecina
                //set_idVecino<<<1, 1>>>(i, numvecinos, j);
                //cudaDeviceSynchronize();
                //set_idVecinoStruct<<<1, 1>>>(i, j, numvecinos);
                //cudaDeviceSynchronize();
                //numvecinos++;
                //printf("Soy %i, y soy %i \t", i, islote[i].tipo_celula);
                //printf("\n");
            } else {
                if (a == 1) {
                    set_idVecino<<<1, 1>>>(i, numvecinos, j);
                    //cudaDeviceSynchronize();
                    set_idVecinoStruct<<<1, 1>>>(i, j, numvecinos);
                    cudaDeviceSynchronize();
                    numvecinos++;
                }
            }
            p = strtok(NULL, " ");
            j++;
        }
        // Guarda el numero total de vecinos de la celula i 
        set_numVecinos<<<1, 1>>>(i, numvecinos);
        i++;
    }
}


__global__ void imprimeredcelula() {
    int j, i;
    for (i = 0; i < totalCelulas; i++) {
        printf("Soy %d, con %d vecinos \t", i, islote[i].n_vecinos);
        for (j = 0; j < maxVecinos; j++) {
            printf("%d ", islote[i].id_vecinos[j]);
        }
        printf("\n");
        //fflush(stdout);
    }
}

__global__ void iniciaredcelula(int i) {
    int j;
    for (j = 0; j < maxVecinos; j++) {
        islote[i].id_vecinos[j] = -1;
    }
    islote[i].n_celula = 0;
    islote[i].n_vecinos = 0;
    //double deltabeta = 2/(totalCelulas-1);
    //islote[i].frec = 1.+beta*(-1.0+(double)i*(2./(totalCelulas-1.)));
    //islote[i].frec = 1./10.;
}

__global__ void set_gacople(int i, double gacople, int numvecinos) {
    // guarda parametro de acople entre celula i y sus vecinos
    islote[i].vecinos[numvecinos].gacople = gacople;
    //printf("Soy %i con gacople = %f\n", i, islote[i].vecinos[numvecinos].gacople);
    printf("%i,%i,%f\n", i, islote[i].id_vecinos[numvecinos],islote[i].vecinos[numvecinos].gacople);
}


__global__ void asignar_theta(int i, double theta){
    // para pasar angulos generados en host a GPU
    islote[i].theta = theta;
    printf("Soy %i con angulo %f\n", i, islote[i].theta);
}

__global__ void asignar_frec(int i, double frec){
    islote[i].frec = frec;
}

void init_theta(){
    // Inicializa angulos para cada celula en host
    double theta;
    double frec;


    for (int i=0; i<totalCelulas; i++){
theta = 2 * PI * get_random();
        //theta = (2*(double)i*PI)/(double)totalCelulas;
        asignar_theta<<<1,1>>>(i, theta);
        cudaDeviceSynchronize();
         frec = 0.0016666666666666668;
        //frec = rand_normal(0.001, 0.005);
        asignar_frec<<<1,1>>>(i, frec);
        //printf("%f\n", theta);
    }

}


void cargarArchivoCoupling() {
    FILE *fp;
    int i = 0;
fp = fopen("/home/gerardo/Documents/IsletLab/H51_Kmat.txt", "r");
    char linea[1000000];
    while (fgets(linea, sizeof(linea), fp)) {
        int numvecinos = 0;
        char *p = strtok(linea, " ");
        int j = 0;
        while (p != NULL) {
            //printf( " %s\t", p );
            double a = atof(p);
                if(a!=0.0){
                //if (a == 1) {
                    set_gacople<<<1, 1>>>(i, a, numvecinos);
                    cudaDeviceSynchronize();
                    //islote[i].vecinos[numvecinos].gacople = a;
                    //printf("gcoup = %f\n", islote[i].vecinos[numvecinos].gacople);
                    numvecinos++;
                }
    
            p = strtok(NULL, " ");
            j++;
        }
        //islote[i].n_vecinos = numvecinos;
        i++;
    }
}


__global__ void calcula_InfluenciaVecinas() {
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int tid = blockId * (blockDim.x * blockDim.y * blockDim.z)
            + (threadIdx.z * (blockDim.x * blockDim.y))
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    int i = tid;

    while (i < totalCelulas) {
        calcular_acople(i);
        i = i + NUMHILOS;
    }

}

__device__ void resolver(int i, double dt, double (*mn)(double (*f)(double, int), double h, double xi,int i)){
    islote[i].theta = mn(dthetadt, dt, islote[i].theta, i);
}


__global__ void actualizaParametros(double dt) {
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int tid = blockId * (blockDim.x * blockDim.y * blockDim.z)
            + (threadIdx.z * (blockDim.x * blockDim.y))
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    int i = tid;

    while (i < totalCelulas) {
        resolver(i, dt, rk4);
        i = i + NUMHILOS;
    }
}



__global__ void getAngulos(double *angulos){
    int i;
    for (i = 0; i < totalCelulas; ++i) {
        angulos[i] = islote[i].theta;
    }
}



int main(void){
    // seed numeros aleatorios
    srand(time(NULL)); // randomize seed

    time_t begin = time(NULL);

    // Tiempo total de simulacion
double Tf = 20000.0;
    double t;
    // Paso de tiempo simulacion
double dt = 0.1;
    int indice = 0;

    // Archivos para guardar 
FILE *salidaAngulosIslote = fopen("/home/gerardo/Documents/IsletLab/H51_kuramoto_angles.data", "w");

    // Memoria
    cudaMalloc((void**) &Angulos_Device, totalCelulas * sizeof(double));
    Angulos_Host = (double*) malloc(totalCelulas * sizeof(double));

    for (int cell = 0; cell < totalCelulas; cell++) {
        iniciaredcelula<<<1, 1>>>(cell);
        cudaDeviceSynchronize();
    }
    
    // Carga matriz de adyacencias y guarda tipo de celulas
    // y vecinos de cada celula
    cargarArchivo();

    // Imprime numero de celula, numero de vecinos e id de vecinos
    imprimeredcelula<<<1,1>>>();
    cudaDeviceSynchronize();

    // Carga los parametros K de los osciladores
    // En islote[i].vecinos[numvecinos].gacople
    // queda guardada la conductancia entre la celula i y 
    // el vecino islote[i].id_vecinos[numvecinos],
    cargarArchivoCoupling();

    // Inicializa angulos (theta)
    init_theta();

    for (t = 0; t < Tf;) {
if (indice % 500 == 0){
            getAngulos<<<1,1>>>(Angulos_Device);
            cudaDeviceSynchronize();

            cudaMemcpy(Angulos_Host, Angulos_Device, totalCelulas * sizeof(double), cudaMemcpyDeviceToHost);
            cudaDeviceSynchronize();
            printf("%lf\n",t); fflush(stdout);
            fprintf(salidaAngulosIslote, "%lf\t", t);
            for (int i = 0; i < totalCelulas; ++i) {
                if (i == totalCelulas - 1) {
                    fprintf(salidaAngulosIslote, "%lf\n", Angulos_Host[i]);
                } else {
                    fprintf(salidaAngulosIslote, "%lf\t", Angulos_Host[i]);
                }
            }
        }

        calcula_InfluenciaVecinas<<<numBlocks, threadsPerBlock>>>();
        cudaDeviceSynchronize();

        actualizaParametros<<<numBlocks, threadsPerBlock>>>(dt);
        cudaDeviceSynchronize();

    
        indice++;
        t = t + dt;

    }
    time_t end = time(NULL);
    printf("Tiempo de ejecucion: %ld segundos\n", (end - begin));
    fflush(stdout);

    return EXIT_SUCCESS;
    
}
