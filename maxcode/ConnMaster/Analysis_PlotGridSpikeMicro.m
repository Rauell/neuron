function [] = Analysis_PlotGridSpikeMicro(s)

load('MICRO_0.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID,s,1)
load('MICRO_10.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_20.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_30.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_40.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_50.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_60.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_70.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_80.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_90.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)
load('MICRO_100.mat')
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, s,1)

ylabel('SPIKE distances', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
xlabel('Stimulus interval (ms)', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
set(gca,'LineWidth',2,'FontSize',14, 'FontWeight', 'bold', 'FontName','Times')
axis([3 102 0 0.3])

if s == 1,
    
   title('Network SPIKE', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
   
elseif s == 2,
    
    title('SPIKEg - X', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
    
elseif s == 3,
    
    title('SPIKEg - Y', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
    
else
    
    title('SPIKEg - Z', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
    
end