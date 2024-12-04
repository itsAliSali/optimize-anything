# optimize-anything
This project allows you to optimize a given objective function using either local optimization (with Scipy) or global optimization (with Pymoo). The program is independent of the objective function, as the objective is written as an external program that can be anything. For demonstration purposes, the [Eggholder benchmark function](https://en.wikipedia.org/wiki/Test_functions_for_optimization) is implemented as the objective function. Objective function evaluations are performed in parallel when possible (e.g., during parallel runs of the PSO population).

## How to Use
1. **Choose your optimizer**:  
   Open the `sample_config.ini` file and set the `method` parameter to either `local` or `global`.

2. **Update the configuration**:  
   Modify the configuration file (`sample_config.ini`) to adjust parameters like max_generations, initial point, timeout, etc., as per your requirements.

3. **Run the script**:  
   Execute the Python script `main.py` to start the optimization process.

   ```bash
   python main.py
   ```

4. **Check the results**:
    After the script finishes, check the results in the optimization log file. This log contains detailed information about the optimization process and results.

## Requirements / Testing
Make sure to install the necessary dependencies by running:
```bash
pip install -r requirements.txt
```
Run the tests using unittest:
```bash
python -m unittest discover -s tests
```

## Further Development
Here are some potential directions for further development:
* Multi-objective optimization
* Adaptive stopping criteria
* Visualization of error through iterations 

## TODO
- [x] implement the obj funtion as a python program
- [x] use scipy to optimize.
- [x] parallelize the program --> scipy does not support evaluating all the population in the objective function. So I'm switching to PyMoo.
- [x] implement PSO in PyMoo
- [x] add timeout mechanism to external function call.
- [x] read optimizaiton params from config file.
- [x] unittest  
- [x] add requirement.txt file
- [x] github action
- [x] write an instruction on how to run the code (Update readme file).

