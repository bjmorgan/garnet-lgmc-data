#! /usr/bin/env python3

import lattice_mc
import multiprocessing
import numpy as np
import sys

k_boltzmann = 8.6173324e-5
temperature = 298.0
kT = k_boltzmann * temperature

def llzo_correlation_calc( options ):

    s = lattice_mc.Simulation()
    s.define_lattice_from_file( options.lattice_site_file, options.lattice_cell_lengths )
    s.set_number_of_atoms( options.number_of_atoms )
    s.set_number_of_jumps( options.number_of_jumps )
    s.set_number_of_equilibration_jumps( options.number_of_equilibration_jumps )
    if options.nn_energy_scaling:
        s.set_nn_energy( options.nn_energy_scaling * kT )
    if options.site_energies:
        s.set_site_energies( options.site_energies )
    if options.setup_lookup_table:
        s.setup_lookup_table()

    s.run()
 
    f = s.tracer_correlation()
    fc = s.collective_correlation()
    d = s.tracer_diffusion_coefficient()
    dc = s.collective_diffusion_coefficient_per_atom()
    occ = s.average_site_occupations()
    #print( f, fc, d, dc )
    return f, fc, d, dc, occ[ 'O' ], sum( [ occ[ s ] for s in [ 'T1', 'T2', 'T3' ] ] ) 

if __name__ == '__main__':
    options = lattice_mc.Options()
    #options.set_number_of_atoms( 416 )
    options.set_nn_energy_scaling( 3.0 )
    #options.set_site_energies( { 'O' : 1.0 * kT, 'T1' : 0.0, 'T2' : 0.0, 'T3' : 0.0 } )
    options.set_number_of_jumps( 10000 )
    options.set_number_of_equilibration_jumps( 1000 )
    options.read_lattice_from_file( 'llzo_lattice_site_list.dat' )
    options.set_lattice_cell_lengths( [ 49.0672361, 49.0672361, 49.0672361 ] )
    options.setup_lookup_table = True

    nproc = 32
    n_samples = 2000

    for number_of_atoms in [ 1, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 575 ]:
        options.set_number_of_atoms( number_of_atoms ) 

        calc_pool = ( options for i in range( n_samples ) )
        pool = multiprocessing.Pool( processes = nproc )
        f_sampled = np.array( pool.map( llzo_correlation_calc, calc_pool ) )
  
        print( 'number of atoms: {}'.format( options.number_of_atoms ) )
        print( 'nearest-neighbour energy scaling (vs kT): {}'.format( options.nn_energy_scaling ) )
        print( 'site energies: {}'.format( options.site_energies ) )
        print( 'number of jumps: {}'.format( options.number_of_jumps ) )
        print( '=> ' + str( sum( f_sampled ) / len( f_sampled ) ) )
        print()
        sys.stdout.flush()
