function [SPIKE, num] = Analysis_GetGridSPIKE(currentDir, Pos, dim, fileIndex, stim, simTime, L, nodes, inhibIndex)
 
%{
    This program will determine the SPIKE distance of a given geometric
    network with regards to spatial organization.  The 3D network will be
    collapsed into a 2D grid, and the grid will have n*n nodes.  The
    neurons will be assigned to nodes respective to their position and the
    dimension in which they are being collapsed.  Each node is then
    evaluated in terms of the SPIKE distance and the resulting SPIKE
    distances are saved.
 
    INPUT
 
    dim : Dimension (x,y, or z) in which the network will be collapsed
    geo : Geometric positions of each neuron
    L   : Length of the cubic neural block
    nodes   : Defines the number of grid points/nodes
    data: Firing data for neurons in the network
%}

%% Step 1 - Load spiking data.
N = length(Pos);  % Get number of neurons
spikes = GetSimulationData(currentDir, N, fileIndex, con, age, stim, simTime, plotornot);

%% Step 2 - Create grid respect to dim. 
if dim == 1,     % Analyze x-direction
    Pos = [Pos(:,2) geo(:,3)];
elseif dim == 2, % Analyze y-direction
    Pos = [Pos(:,1) geo(:,3)];
else             % Analyze z-direction
    Pos = [Pos(:,1) geo(:,2)];
end
b = L/(n-1);  % Length of each node.
c = b/2;      % Useful for speeding up calculations later
grid = zeros(nodes, nodes, 2);
for i = 1 : nodes,
    for j = 1 : nodes,
        grid(i,j,2) = (i-1)*b + c;
        
        grid(i,j,1) = (j-1)*b + c;
        
    end
end

%% Step 3 - Assign neurons to node points.
hold on
SPIKE = zeros(i-1,j-1); % Initialize SPIKE matrix
num = zeros(i-1,j-1);
total = 0;
for i = 1:n-1, 
    for j = 1:n-1, % Iterate through all nodes
        
        temp = zeros(1,1); % Temp matrix to store neural indices
        count = 1;
        
        for k = 1:N, % Iterate through all neurons
            
            [temp, count] = GetInGrid(Pos(k,:), grid(i,j,1), grid(i,j,2), L, b, c, temp, count, k, inhibIndex);

        end
        
        if length(temp) > 1,

            try
                
                s = spikes(temp, :);
                results=f_distances_MEX(s,d_para,f_para);
                num(i,j) = length(temp);
                SPIKE(i,j) = results.overall_dissimilarities;
                
            catch
                
                i
                j
                temp
                s = spikes(temp, :)
                disp('something done messed up')            
                results=f_distances_MEX(s,d_para,f_para);
                SPIKE(i,j) = results.overall_dissimilarities;
                
            end
            
        end
        
        total = total + length(temp);
    end
end
 
disp('done!')