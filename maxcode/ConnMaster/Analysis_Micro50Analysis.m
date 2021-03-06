hold on

% First plot old Micro 50
load('MICRO_50.mat')
subplot(2,2,1)
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, 1,1)
subplot(2,2,2)
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, 2,1)
subplot(2,2,3)
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, 3,1)
subplot(2,2,4)
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, 4,1)

% First plot old Micro 50
load('MICRO_50_new.mat')
subplot(2,2,1)
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, 1,2)
title('Network SPIKE', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
ylabel('SPIKE distances', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
xlabel('Stimulus interval (ms)', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
set(gca,'LineWidth',2,'FontSize',14, 'FontWeight', 'bold', 'FontName','Times')
axis([3 102 0 0.3])

subplot(2,2,2)
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, 2,2)
title('SPIKEg - X', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
ylabel('SPIKE distances', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
xlabel('Stimulus interval (ms)', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
set(gca,'LineWidth',2,'FontSize',14, 'FontWeight', 'bold', 'FontName','Times')
axis([3 102 0 0.3])

subplot(2,2,3)
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, 3,2)
title('SPIKEg - Y', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
ylabel('SPIKE distances', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
xlabel('Stimulus interval (ms)', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
set(gca,'LineWidth',2,'FontSize',14, 'FontWeight', 'bold', 'FontName','Times')
axis([3 102 0 0.3])

subplot(2,2,4)
Analysis_MeanAndStd(SPIKE, SPIKE_GRID, 4,2)
title('SPIKEg - Z', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
ylabel('SPIKE distances', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
xlabel('Stimulus interval (ms)', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
set(gca,'LineWidth',2,'FontSize',14, 'FontWeight', 'bold', 'FontName','Times')
axis([3 102 0 0.3])
%legend('Normal Strength', '80% Normal Strength')