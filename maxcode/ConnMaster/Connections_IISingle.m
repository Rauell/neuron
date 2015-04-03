function C = ConnectIISingle(Dz, Dxy, con)

%{
    This program will determine the connectivity between a single pair of
    inhibitory neurons.  This connection will follow Rieubland et al 2014 
    using the 'non-uniform random' model.  Connectivity for electric or
    chemical synapses will depend soley on the distances in the z and xy
    planes.
   
    Max Henderson
    May 19, 2014
    Drexel University
%}

m = 2; % Multiplier constant to insure a certain level of connecitvity

if con == 1, % Electric
    
    if Dz >= 30,
        
        C = 0;
        
    else
        
        if Dz <= 10,
            
            p = 0.7 - (0.7/150)*Dxy;
            
            r = rand(1,1);
            
        elseif Dz <= 20
            
            p = 0.5 - (0.5/120)*Dxy;
            
            r = rand(1,1);
            
        else
            
            p = 0.4 - (0.4/75)*Dxy;
            
            r = rand(1,1);
            
        end
        
        p = p*m;
        
        if p > r,
                   
            C = 1;
                
        else
            
            C = 0;
                
        end
        
    end
else % Chemical
        
    if Dz >= 40,
        
        C = 0;
        
    else
        
        if Dz <= 20,
            
            p = 0.3 - (0.3/170)*Dxy;
            
            r = rand(1,1);
            
        else
            
            p = 0.2 - (0.2/120)*Dxy;
            
            r = rand(1,1);
            
        end
        
        p = p*m;
        
        if p > r,
                   
            C = 1;
                
        else
            
            C = 0;
                
        end
        
    end
end