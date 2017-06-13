#! /usr/bin/env ruby

require 'yaml'

length_scaling = 1e-10 # Assume we are converting Angstroms to m.

filename = ARGF.argv[0]

columns = [ 'n_Li', 'E_nn', 'E_site', 'f', 'f_I', 'D_t', 'D_coll', 'n_oct', 'n_tet' ]
puts '#' + columns.map{ |s| s.rjust(11) }.join('  ')[1..-1] 
puts

File.open( filename ) do |yf|
  YAML.load_documents( yf ) do |d|
    d['tracer diffusion coefficient'] *= length_scaling**2
    d['collective diffusion coefficient'] *= length_scaling**2
    output = [ d['number of atoms'].to_s,
               d['nearest-neighbour energy scaling'].to_s,
               ( d['site energies']['O'] - d['site energies']['T'] ).to_s,
               '%.3f' %d['correlation factor'],
               '%.3f' %d['collective correlation factor'],
               '%.3e' %d['tracer diffusion coefficient'],
               '%.3e' %d['collective diffusion coefficient'],
               '%.2f' %d['average octahedra occupation'],
               '%.2f' %d['average tetrahedra occupation'] ]
    puts output.map{ |s| s.rjust(11) }.join('  ')
  end
end

