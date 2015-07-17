function geo = PerturbGeo(geo, L, l)

%{
    This program will take a set of 3D coordinates for neurons contained in
    a box of length L and being evaluated on a grid wherein each grid node
    is a l-by-l box.  To account for inconsistencies in initial positions,
    we will perturb the geometry by shifting all of the points randomly.
 
    INPUT
    
    geo : Geometric positions of each neuron
    L   : Length of the cubic neural block
    l   : Length of grid node 

    OUPUT 

    geo : New geometric positions, perturbed by some random displacement
    vector

    Max Henderson
    10/8/14
    Drexel University
%}

%% Generate random perturbation vector.
perturbR = (rand(1,3) - rand(1,3))*l*0.5; % Multiply by 1/2 the length of grid node length

%% Perturb geo by perturbR.
for i = 1:size(geo,1),
    
    % Perturb..
    geo(i,:) = geo(i,:) - perturbR;
    
    % And account for both types of boundary conditions...
    geo(i,:) = AccountForBC(geo(i,:), L);
    
end