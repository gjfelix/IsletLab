 ```
  ___     _      _   _          _        _   _  
 |_ _|___| | ___| |_| |    __ _| |__    (_)_(_) 
  | |/ __| |/ _ \ __| |   / _` | '_ \  (_) _ (_)
  | |\__ \ |  __/ |_| |__| (_| | |_) |  | (_) | 
 |___|___/_|\___|\__|_____\__,_|_.__/  (_)___(_)
                                        (_) (_)  v1.0
 ```

![IsletLab Interface](GUI_FullWindow.png)

### Isletlab Project

This software is licensed under the GPL V3 Open Source Licence

Project created by:

**Gerardo J. Félix-Martínez**
Consejo Nacional de Ciencia y Tecnología (México)
Universidad Autónoma Metropolitana, Iztapalapa.

[Google Scholar](https://scholar.google.com/citations?user=wcuaM4QAAAAJ&hl=en&authuser=1) 

Website:<https://gjfelix.github.io>

Email: gjfelix2005@gmail.com

Last update: March 2022

====================================================================

[IsletLab Documentation](https://github.com/gjfelix/IsletLab/wiki)

====================================================================

Current version of Isletlab has been fully tested in Ubuntu Linux 18, Windows 11 and MacOS Catalina

**Requirements:**

- [ ] [Anaconda](https://anaconda.org/) (Python 3.8) 
- [ ] GCC compiler
- [ ] NVCC compiler ([CUDA toolkit](https://developer.nvidia.com/cuda-toolkit))
- [ ] [CUDA capable NVIDIA GPU Device](https://developer.nvidia.com/cuda-gpus)



====================================================================

**Testing installation**

Sample data is included in the repository to test IsletLab. 

1. Click the "Load initial islet" button

2. Select the "H51.txt" file containing the test data and click "Open".

   If everything works as intended, a plot of the initial islet should be visible.

3. Click the "Reconstruction settings" button.

   - Change the number of threads to match the processor characteristics and click OK. 

4. Click the "Reconstruct islet" button to open the "Reconstruction Log" window.

5. Click the "Run" button. 

   - Check that the IsletLab version appears at the "Reconstruction Log" window.
   - Check that the number of overlapped cells in the initial islets is printed.
   - For each iteration of the optimization algorithm the number of overlapped cells must be printed.
   - Once the reconstruction is finished, the total "Computing time" is printed.

6. Close the "Reconstruction Log " window.

7. Click the "Cell-to-cell contacts" button.

8. Click the "Build Network" button.

9. Switch to the "Simulation" tab. (Only activated is a CUDA-capable NVIDIA video card is available).

10. Configure the number of Blocks and Threads (depends on the NVIDIA card model).

11. Click "Run Simulation" to open the "Simulation Log" window and click "Run". 

12. Close the "Simulation Log" window once the calculation finishes.

If all the steps were performed correctly, IsletLab was correctly installed.

====================================================================

Please, if you are unable to run IsletLab or you have any problem do not hesitate to send me an email (<gjfelix2005@gmail.com>). 

In case you find a bug or want to contribute with an idea or request, please [create an issue](https://github.com/gjfelix/IsletLab/issues).

