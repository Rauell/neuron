function [N1, N2, Ndiag, Dtemp] = GetConDim(connStruct, choice)

%{
    This program will return the dimensions of the particular connectivity
    matrix of choice, as well as how many neurons have to be accounted for
    along the diagonal (if EE or II).

    INPUT

    connStruct = Connectivity structure with several fields determining
    types of connectivity networks
    choice = Defining whether we care about EE, EI, IE or II connections
        1 = EE
        2 = EI
        3 = IE
        4 = II

    OUTPUT

    N1 = Number of rows in current connectivity matrix
    N2 = Number of columns in current connectivity matrix
    Ndiag = Number of diagonal neurons to exclude connecting (no auto-syn)
    Dtemp = Distance matrix depending on type

    Max Henderson and Micheal Royster
    Drexel University
    Last updated March 23, 2015
%}
if choice == 1, % EE
    
    N1 = connStruct.NE;
    N2 = connStruct.NE;
    Ndiag = connStruct.NE;
    if connStruct.Dchoice(1) == 1,
        
        Dtemp = connStruct.DEEz;
        
    elseif connStruct.Dchoice(1) == 2,
        
        Dtemp = connStruct.DEExy;
        
    else
        
        Dtemp = connStruct.DEE;
        
    end
    
elseif choice == 2, % EI
    
    N2 = connStruct.NI;
    N1 = connStruct.NE;
    Ndiag = 0;
    if connStruct.Dchoice(2) == 1,
        
        Dtemp = connStruct.DEIz;
        
    elseif connStruct.Dchoice(2) == 2,
        
        Dtemp = connStruct.DEIxy;
        
    else
        
        Dtemp = connStruct.DEI;
        
    end
    
elseif choice == 3, % IE
    
    N2 = connStruct.NE;
    N1 = connStruct.NI;
    Ndiag = 0;
    if connStruct.Dchoice(3) == 1,
        
        Dtemp = connStruct.DIEz;
        
    elseif connStruct.Dchoice(3) == 2,
        
        Dtemp = connStruct.DIExy;
        
    else
        
        Dtemp = connStruct.DIE;
        
    end
    
else % II
    
    N1 = connStruct.NI;
    N2 = connStruct.NI;
    Ndiag = connStruct.NI;
    if connStruct.Dchoice(4) == 1,
        
        Dtemp = connStruct.DIIz;
        
    elseif connStruct.Dchoice(4) == 2,
        
        Dtemp = connStruct.DIIxy;
        
    else
        
        Dtemp = connStruct.DII;
        
    end
    
end