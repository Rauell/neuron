function D = CalculatePeriodicDistances(N, pos, a, xyz)

%{
    This program will determine the intersomatic distances between neurons
    in the network using periodic boundary conditions, assuming isotropic
    connectivity.

    INPUT
    
    N : Number of neurons in network
    pos : Positions of neurons in respective network
    a : length of one side of the cubic volume in which all neurons reside
    xyz = 1     :   Return z-distances
    xyz = 2     :   Return xy-distances
    xyz = 3     :   Return xyz-distances

    OUTPUT

    D : N-by-N matrix of distances between neurons

    Max Henderson and Michael Royster
    Last updated: March 6, 2015
    Drexel University
%}

% Initializing return matrix
D = zeros(N);

% Initialzing useful variable
a2 = a*0.5;

% Calculating periodic distances between z values
if xyz == 1,
    % from 1 to N-1
    for i = 1:N-1,
        % from i+1 to N
       for j = i+1:N,
           % Calculating absolute z distance
           dend = abs(pos(i,3)-pos(j,3));
           
           % Ensuring periodic boundary conditions
           if dend > a2,
               dend = a - dend;
           end
           
           D(i, j) = dend;
           D(j, i) = dend;
       end
    end
elseif xyz == 2, % Distances in xy-plane...
    % from 1 to N-1
    for i = 1:N-1,
        % from i+1 to N
       for j = i+1:N,
           % Calculating absolute z distance
           x = abs(pos(i,1)-pos(j,1));
           y = abs(pos(i,2)-pos(j,2));
           
           % Ensuring periodic boundary conditions
           if x > a2,
               x = a - x;
           end
           if y > a2,
               y = a - y;
           end
           
           dend = sqrt(x*x + y*y); 
           
           D(i, j) = dend;
           D(j, i) = dend;
       end
    end
else % 3D distances...
    % from 1 to N-1
    for i = 1:N-1,
        % from i+1 to N
       for j = i+1:N,
           % Calculating absolute z distance
           x = abs(pos(i,1)-pos(j,1));
           y = abs(pos(i,2)-pos(j,2));
           z = abs(pos(i,3)-pos(j,3));
           
           % Ensuring periodic boundary conditions
           if x > a2,
               x = a - x;
           end
           if y > a2,
               y = a - y;
           end
           if z > a2,
               z = a - z;
           end
           
           dend = sqrt(x*x + y*y + z*z); 
           
           D(i, j) = dend;
           D(j, i) = dend;
       end
    end
end