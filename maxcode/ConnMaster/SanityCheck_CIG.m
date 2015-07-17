function CIG = SanityCheck_CIG(C, Pos, connStruct)

curL = connStruct.L;
node = 12;
inhib = connStruct.NE + 1;

% With connectivity, determine CIGx...
disp('CIG in x direction...')
CIG = GetCIG(Pos,       C, curL, node, inhib, 1)

% With connectivity, determine CIGy...
disp('CIG in y direction...')
CIG  = GetCIG(Pos,       C, curL, node, inhib, 2)

% With connectivity, determine CIGz...
disp('CIG in z direction...')
CIG  = GetCIG(Pos,       C, curL, node, inhib, 3)