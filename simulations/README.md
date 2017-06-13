# Example scripts for running lattice-gas Monte Carlo simulations on a garnet lattice

## Contents

| filename                       | description                                         |
|--------------------------------|-----------------------------------------------------|
| `README.md`                    | This file.                                          |
| `garnet_lattice_lgmc.py`       | Simulation script.                                  |
| `lgmc_output.yml`              | Example output YAML file.                           |
| `garnet_lattice_site_list.dat` | Site-list file for 2x2x2 cubic-LLZO.                |
| `lattice_yaml_to_csv.rb`       | Script to convert the YAML output to formatted CSV. |
| `requirements.txt`             | List of Python package dependencies.                |

The `garnet_lattice_lgmc.py` script contains an example for running a series of `lattice_mc` lattice-gas Monte Carlo simulations \[1\]. 

## Running
```
./garnet_lattice_lgmc.py > lgmc_output.yml
```

## Settings
Most simulation parameters are set at the top of the file:
```
atom_numbers = [ 1, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 575 ]
nn_energy    = 0.0   # units of kT
delta_e_site = 0.0   # units of kT
n_jumps      = 10000 # number of jumps in the production run
n_eq_jumps   = 1000  # number of equilibration jumps
n_samples    = 100   # number of equivalent simulations per paramter set to average over

nproc = 32 # parallelise over processors
```

The script depends on the `garnet_lattice_site_list.dat` file, which contains data defining the lattice site coordinates and connectivity for a 2x2x2 cubic LLZO cell.

The script loops over the entries in `atom_numbers` and performs `n_samples` simulations for each set of parameters. The nearest-neighbour interaction energy and difference in site energies (octahedral versus tetrahedral) are set using `nn_energy` and `delta_e_site` respectively. Both these energies are rescaled by _kT_ for the simulations.

The script uses the `multiprocessing` package to perform parallel simulations over multiple shared-memory cores (if present). The number of cores to be used is set using `nproc`.

The output is human-readable YAML, with a separate entry for each set of simulation paramaters, e.g.
```
---
number of atoms: 192
nearest-neighbour energy scaling: 0.0
site energies:
    O: 0.0
    T: 0.0
number of jumps: 10000
correlation factor: 0.7253937551714361
collective correlation factor: 0.9571663892650695
tracer diffusion coefficient: 30470202681255.227
collective diffusion coefficient: 40294452653148.57
average octahedra occupation: 128.0174243655277
average tetrahedra occupation: 63.982575634472404
```

This output can be converted into formatted CSV using the `lattice_yaml_to_csv.rb` script, e.g.
```
./lattice_yaml_to_csv.rb lgmc_output.yml
```

to produce

```
#      n_Li         E_nn       E_site            f          f_I          D_t       D_coll        n_oct        n_tet

          1          0.0          0.0        1.012        1.012    6.368e-07    6.368e-07         0.67         0.33
         32          0.0          0.0        0.951        1.096    5.667e-07    6.533e-07        21.33        10.67
         64          0.0          0.0        0.910        0.993    5.099e-07    5.564e-07        42.67        21.33
         96          0.0          0.0        0.853        1.026    4.475e-07    5.386e-07        64.01        31.99
        128          0.0          0.0        0.813        0.962    3.986e-07    4.719e-07        85.30        42.70
        160          0.0          0.0        0.763        0.963    3.476e-07    4.390e-07       106.61        53.39
        192          0.0          0.0        0.725        0.957    3.047e-07    4.029e-07       128.02        63.98
        224          0.0          0.0        0.672        0.998    2.586e-07    3.851e-07       149.30        74.70
        256          0.0          0.0        0.634        1.000    2.221e-07    3.496e-07       170.69        85.31
        288          0.0          0.0        0.590        0.861    1.863e-07    2.719e-07       191.94        96.06
        320          0.0          0.0        0.551        1.224    1.544e-07    3.428e-07       213.23       106.77
        352          0.0          0.0        0.515        1.111    1.263e-07    2.728e-07       234.69       117.31
        384          0.0          0.0        0.476        0.983    9.990e-08    2.062e-07       255.95       128.05
```

## Requirements
- `numpy`
- `lattice_mc`: This can be installed using `pip install lattice-mc`, or downloaded from [GitHub](10.5281/zenodo.596979).

## References

1. Morgan, B. J. *`lattice_mc`: A Python Lattice-Gas Monte Carlo Module*, [J. Open Source Software, 2, 00247 (2017)](https://doi.org/10.21105/joss.00247)

