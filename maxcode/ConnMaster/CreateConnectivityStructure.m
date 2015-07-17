function connStruct = CreateConnectivityStructure()

%{
    This program will be used to initialize the most important structure
    for the Master Connectivity code - the connectivity structure, connStruct.  
    This structure will contain in a simple way all the basic information
    for the types of networks that are desired.

    INPUT

    {}

    OUTPUT

    connStruct : Connectivity structure with several fields determining
    types of connectivity networks...
    
    FIELDS

    globalConnectivity = (# connections in network) / (total possible cons)
    connDistribution = % of connections by type, E->E, E->I, I->E, and I->I
    CEE = Type of connectivity for the E->E connections
    CEI = Type of connectivity for the E->I connections
    CIE = Type of connectivity for the I->E connections
    CII = Type of connectivity for the I->I connections
    CN = Method for connecting input matrix into common neighbor law
    Dchoice = Distance matrix to use for each type of connectivity; 1, 2,
    or 3D
    N = Number of neurons in network
    NE = Number of excitory neurons
    NI = Number of inhibitory neurons
    Dz = N-by-N 1D distance matrix
    Dxy = N-by-N 2D distance matrix
    D = N-by-N 3D distance matrix
    DEEz = NE-by-NE distance matrix of 1D distances
    DEIz = NE-by-NI distance matrix of 1D distances
    DIEz = NI-by-NE distance matrix of 1D distances
    DIIz = NI-by-NI distance matrix of 1D distances
    DEExy = NE-by-NE distance matrix of 2D distances
    DEIxy = NE-by-NI distance matrix of 2D distances
    DIExy = NI-by-NE distance matrix of 2D distances
    DIIxy = NI-by-NI distance matrix of 2D distances
    DEE = NE-by-NE distance matrix of 3D distances
    DEI = NE-by-NI distance matrix of 3D distances
    DIE = NI-by-NE distance matrix of 3D distances
    DII = NI-by-NI distance matrix of 3D distances
    threshProb = Matrix describing threshold connectivity probability
    L = Length of box in which original neurons were created
    ID = Matrix containing micrcolumnar IDs for all neurons
    x = Percent of connections to add in addition to microcolumnar
    connections
    SEE_mean = Mean strength of EE connections
    SEI_mean = Mean strength of EI connections
    SIE_mean = Mean strength of IE connections
    SII_mean = Mean strength of EE connections
    SEE_std = Std of EE connections
    SEI_std = Std of EI connections
    SIE_std = Std of IE connections
    SII_std = Std of EE connections
    Rand = Flag to make random networks (or not)
    inputDir = Input directory to get files
    outputDir = Output directory for generated connectivities

    Max Henderson and Michael Royster
    Last updated: March 26, 2015
    Drexel University
%}

%% Create connStruct and initialize with default parameters.
connStruct = struct('gc', 0.02, ... % Range from 0 to 1. 
'connDistribution', [0.75 0.1 0.1 0.05], ... % Range from 0 to 1 for each field, and the vector must be normalized to 1.
'CEE', 1, ... % Range from 1 to 11
'CEI', 1, ... % Range from 1 to 11 
'CIE', 1, ... % Range from 1 to 11
'CII', 1, ... % Range from 1 to 11
'CN', [2 2 2 2],... % Range from 1 to 11 for each part of the vector
'Dchoice', [3 3 3 3], ... % Range from 1 to 3
'N', 0, ... % Number of neurons - no specific range
'NE', 0, ... % Number of neurons - no specific range
'NI', 0, ... % Number of neurons - no specific range
'Dz', 0, ... % N-by-N 1D distance matrix
'Dxy', 0, ... % N-by-N 2D distance matrix
'D', 0, ... % N-by-N 3D distance matrix
'DEEz', 0, ... % NE-by-NE distance matrix of 1D distances
'DEIz', 0, ... % NE-by-NI distance matrix of 1D distances
'DIEz', 0, ... % NI-by-NE distance matrix of 1D distances
'DIIz', 0, ... % NI-by-NI distance matrix of 1D distances
'DEExy', 0, ... % NE-by-NE distance matrix of 2D distances
'DEIxy', 0, ... % NE-by-NI distance matrix of 2D distances
'DIExy', 0, ... % NI-by-NE distance matrix of 2D distances
'DIIxy', 0, ... % NI-by-NI distance matrix of 2D distances
'DEE', 0, ... % NE-by-NE distance matrix of 3D distances
'DEI', 0, ... % NE-by-NI distance matrix of 3D distances
'DIE', 0, ... % NI-by-NE distance matrix of 3D distances
'DII', 0, ... % NI-by-NI distance matrix of 3D distances
'threshProb', [0.3 0.3 0.3 0.3], ... % Range from 0 to 1
'L', 100, ... % No true bounds
'ID', 0, ... % From -1 to max # microcolumns
'x', 0, ... % From 0 to inf
'SEE_mean', 0.05, ... % No true bounds
'SEI_mean', 0.2, ... % No true bounds
'SIE_mean', -0.05, ... % No true bounds
'SII_mean', -0.1, ... % No true bounds
'SEE_std', 0.01, ... % No true bounds
'SEI_std', 0.04, ... % No true bounds
'SIE_std', 0.01, ... % No true bounds
'SII_std', 0.02, ... % No true bounds
'Rand', 0, ... % 0 or 1
'inputDir', 'default', ... % any particular string
'outputDir', 'default'); % any particular string