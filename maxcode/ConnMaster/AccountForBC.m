function geo = AccountForBC(geo, L)

%{
    This program will account for periodic boundary conditions of a single
    neuron.
 
    INPUT
    
    geo : 3D positions of single neuron.
    L   : Length of box neurons are in

    OUPUT 

    geo : 3D positions with BC adjusted for.

    Max Henderson
    10/8/14
    Drexel University
%}

%% Account for BC for each dimension.
for i = 1:3,
    
    % Is > L?
    if geo(1,i) > L,
        geo(1,i) = geo(1,i) - L;
    end
    
    % Is < 0?
    if geo(1,i) < 0,
        geo(1,i) = L + geo(1,i);
    end
    
end