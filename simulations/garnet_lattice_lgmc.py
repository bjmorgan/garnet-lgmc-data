#! /usr/bin/env python3

import lattice_mc
import multiprocessing
import numpy as np
import sys

atom_numbers = [ 1, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 544, 575 ]
nn_energy    = 0.0   # units of kT
delta_e_site = 0.0   # units of kT
n_jumps      = 10000 # number of jumps in the production run
n_eq_jumps   = 1000  # number of equilibration jumps
n_samples    = 100   # number of equivalent simulations per paramter set to average over

nproc = 32 # parallelise over processors

k_boltzmann = 8.6173324e-5
temperature = 298.0
kT = k_boltzmann * temperature

def setup_options():
    options = lattice_mc.Options()
    options.set_nn_energy_scaling( nn_energy )
    options.set_site_energies( { 'O' : delta_e_site, 'T' : 0.0 } )
    options.set_number_of_jumps( n_jumps )
    options.set_number_of_equilibration_jumps( n_eq_jumps )
    options.read_lattice_from_file( 'garnet_lattice_site_list.dat' )
    options.set_lattice_cell_lengths( [ 49.0672361, 49.0672361, 49.0672361 ] )
    options.setup_lookup_table = True
    return options

def llzo_correlation_calc( options ):
    # initialise the simulation
    s = lattice_mc.Simulation()
    s.define_lattice_from_file( options.lattice_site_file, options.lattice_cell_lengths )
    s.set_number_of_atoms( options.number_of_atoms )
    s.set_number_of_jumps( options.number_of_jumps )
    s.set_number_of_equilibration_jumps( options.number_of_equilibration_jumps )
    if options.nn_energy_scaling:
        s.set_nn_energy( options.nn_energy_scaling * kT )
    if options.site_energies:
        site_energies = { k: v*kT for k, v, in options.site_energies.items() }
        s.set_site_energies( options.site_energies )
    if options.setup_lookup_table:
        s.setup_lookup_table()
    # run the simulation
    s.run()
    # collect simulation data 
    f = s.tracer_correlation
    fc = s.collective_correlation
    d = s.tracer_diffusion_coefficient
    dc = s.collective_diffusion_coefficient_per_atom
    occ = s.average_site_occupations
    return f, fc, d, dc, occ[ 'O' ], occ[ 'T' ] 

def output_as_yaml( options, f, fc, d, dc, occ_O, occ_T ):
    print( '---' )
    print( 'number of atoms: {}'.format( options.number_of_atoms ) )
    print( 'nearest-neighbour energy scaling: {}'.format( options.nn_energy_scaling ) )
    print( 'site energies:' )
    for k, v in options.site_energies.items():
        print( '    {}: {}'.format( k, v ) )
    print( 'number of jumps: {}'.format( options.number_of_jumps ) )
    print( 'correlation factor: {}'.format( f ) )
    print( 'collective correlation factor: {}'.format( fc ) )
    print( 'tracer diffusion coefficient: {}'.format( d ) )
    print( 'collective diffusion coefficient: {}'.format( dc ) )
    print( 'average octahedra occupation: {}'.format( occ_O ) )
    print( 'average tetrahedra occupation: {}'.format( occ_T ) )
    print()
    sys.stdout.flush()

if __name__ == '__main__':
    options = setup_options()
    for number_of_atoms in atom_numbers:
        options.set_number_of_atoms( number_of_atoms ) 
        calc_pool = ( options for i in range( n_samples ) )
        pool = multiprocessing.Pool( processes = nproc )
        f_sampled = np.array( pool.map( llzo_correlation_calc, calc_pool ) )
        f, fc, d, dc, occ_O, occ_T = sum( f_sampled ) / len ( f_sampled )
        output_as_yaml( options, f, fc, d, dc, occ_O, occ_T )

