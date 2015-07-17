function s = GetSynapticStrength(i,j,connStruct)

if i <= connStruct.NE,
    if j <= connStruct.NE,
        s = normrnd(connStruct.SEE_mean, connStruct.SEE_std);
    else
        s = normrnd(connStruct.SEI_mean, connStruct.SEI_std);
    end
else
    if j <= connStruct.NE,
        s = normrnd(connStruct.SIE_mean, connStruct.SIE_std);
    else
        s = normrnd(connStruct.SII_mean, connStruct.SII_std);
    end
end